// 迫真戦記 ver0.67 研究知識ベースを Ghidra のプログラムに反映する（Claude 2026-10-29）
//
// 使い方（GUI）: Script Manager の「Script Directories」に knowledge\tools を追加し、
//   Vahren.exe を開いた状態で ApplyKnowledge.java を実行する。
// 使い方（headless）: analyzeHeadless <project> <name> -process -noanalysis
//   -scriptPath <knowledge\tools> -postScript ApplyKnowledge.java
//
// 読むもの: knowledge\generated\ghidra\kb_symbols.tsv / kb_structs.tsv / kb_comments.tsv
//   （knowledge\tools\build_kb.py が作る。手で編集しない）
// すること:
//   - 関数・位置・グローバルに名前を付ける（既存の手作業の名前は上書きしない。--force で上書き）
//   - 説明と「どの資料で話題になっているか」を、関数の先頭のコメント（plate）に書く
//   - 構造体 /Hakushin/UnitDef など を作る（既存の同名は置き換える）
// 何度実行してもよい。コメントは【KB】〜【/KB】の範囲だけを書き換える。
// @category Hakushin

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.data.*;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.SourceType;
import ghidra.program.model.symbol.Symbol;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.*;

public class ApplyKnowledge extends GhidraScript {

    private static final String BEGIN = "【KB】";
    private static final String END = "【/KB】";

    @Override
    public void run() throws Exception {
        boolean force = false;
        for (String a : getScriptArgs()) {
            if (a.equals("--force")) force = true;
        }
        File dir = new File(getSourceFile().getParentFile().getParentFile().getFile(false), "generated" + File.separator + "ghidra");
        File symFile = new File(dir, "kb_symbols.tsv");
        File stFile = new File(dir, "kb_structs.tsv");
        File cmFile = new File(dir, "kb_comments.tsv");
        if (!symFile.isFile()) {
            printerr("見つかりません: " + symFile + "（先に build_kb.py を実行してください）");
            return;
        }
        int named = 0, kept = 0, created = 0, labels = 0, comments = 0, failed = 0;
        List<String> failures = new ArrayList<>();
        for (String line : Files.readAllLines(symFile.toPath(), StandardCharsets.UTF_8)) {
            if (line.isEmpty()) continue;
            String[] p = line.split("\t", -1);
            if (p.length < 4) continue;
            Address ad = toAddr(Long.parseLong(p[0], 16));
            String kind = p[1], name = p[2], cm = p[3];
            try {
                if (kind.equals("func")) {
                    Function f = getFunctionAt(ad);
                    if (f == null) {
                        f = createFunction(ad, null);
                        if (f != null) created++;
                    }
                    if (f != null) {
                        boolean userNamed = f.getSymbol().getSource() == SourceType.USER_DEFINED
                                && !f.getName().equals(name) && !f.getName().startsWith("FUN_");
                        if (userNamed && !force) {
                            kept++;
                        } else if (!f.getName().equals(name)) {
                            f.setName(name, SourceType.USER_DEFINED);
                            named++;
                        }
                    }
                } else if (kind.equals("global") || kind.equals("object") || kind.equals("code") || kind.equals("string")) {
                    Symbol s = createLabel(ad, name, true);
                    if (s != null) labels++;
                }
                if (!cm.isEmpty()) {
                    if (kind.equals("code")) {
                        setPreComment(ad, merge(getPreComment(ad), cm));
                    } else {
                        setPlateComment(ad, merge(getPlateComment(ad), cm));
                    }
                    comments++;
                }
            } catch (Exception e) {
                failed++;
                if (failures.size() < 20) failures.add(p[0] + " " + name + ": " + e.getMessage());
            }
        }
        // 命令名などの短いコメント（2026-10-11 の分）
        int pre = 0;
        if (cmFile.isFile()) {
            for (String line : Files.readAllLines(cmFile.toPath(), StandardCharsets.UTF_8)) {
                String[] p = line.split("\t", 2);
                if (p.length < 2) continue;
                Address ad = toAddr(Long.parseLong(p[0], 16));
                try {
                    setPreComment(ad, merge(getPreComment(ad), p[1]));
                    pre++;
                } catch (Exception e) {
                    failed++;
                }
            }
        }
        int structs = applyStructs(stFile);
        println(String.format("ApplyKnowledge: 名前 %d（手作業の名前を保持 %d、関数を新規作成 %d）、ラベル %d、コメント %d、短いコメント %d、構造体 %d、失敗 %d",
                named, kept, created, labels, comments, pre, structs, failed));
        for (String f : failures) println("  失敗: " + f);
    }

    private String merge(String old, String add) {
        String base = old == null ? "" : old;
        int b = base.indexOf(BEGIN), e = base.indexOf(END);
        if (b >= 0 && e > b) {
            base = (base.substring(0, b) + base.substring(e + END.length())).trim();
        }
        String block = BEGIN + "\n" + add.replace(" // ", "\n") + "\n" + END;
        return base.isEmpty() ? block : base + "\n" + block;
    }

    private DataType typeOf(String t) {
        switch (t) {
            case "u8": return ByteDataType.dataType;
            case "i32": return IntegerDataType.dataType;
            case "u32": return DWordDataType.dataType;
            case "ptr": return PointerDataType.dataType;
            case "i32x15": return new ArrayDataType(IntegerDataType.dataType, 15, 4);
            default: return null;
        }
    }

    private int applyStructs(File stFile) throws Exception {
        if (!stFile.isFile()) return 0;
        Map<String, List<String[]>> by = new LinkedHashMap<>();
        for (String line : Files.readAllLines(stFile.toPath(), StandardCharsets.UTF_8)) {
            String[] p = line.split("\t", -1);
            if (p.length < 5) continue;
            by.computeIfAbsent(p[0], k -> new ArrayList<>()).add(p);
        }
        DataTypeManager dtm = currentProgram.getDataTypeManager();
        CategoryPath cat = new CategoryPath("/Hakushin");
        int n = 0;
        for (Map.Entry<String, List<String[]>> en : by.entrySet()) {
            int size = 4;
            for (String[] p : en.getValue()) {
                int off = Integer.parseInt(p[1]);
                int len = p[2].equals("str") ? 0x18 : p[2].equals("i32x15") ? 60 : p[2].equals("rect[]") ? 16 : p[2].equals("u8") ? 1 : 4;
                size = Math.max(size, off + len);
            }
            StructureDataType s = new StructureDataType(cat, en.getKey(), size);
            for (String[] p : en.getValue()) {
                int off = Integer.parseInt(p[1]);
                String nm = p[3], cm = p[4];
                try {
                    if (p[2].equals("str")) {
                        // std::string（本体 16 バイト、+0x10 長さ、+0x14 容量）
                        s.replaceAtOffset(off, new ArrayDataType(CharDataType.dataType, 16, 1), 16, nm + "_buf", cm);
                        s.replaceAtOffset(off + 0x10, DWordDataType.dataType, 4, nm + "_len", "std::string の長さ");
                        s.replaceAtOffset(off + 0x14, DWordDataType.dataType, 4, nm + "_cap", "std::string の容量");
                    } else if (p[2].equals("rect[]")) {
                        s.replaceAtOffset(off, new ArrayDataType(DWordDataType.dataType, 4, 4), 16, nm, cm);
                    } else {
                        DataType dt = typeOf(p[2]);
                        if (dt == null) dt = Undefined4DataType.dataType;
                        s.replaceAtOffset(off, dt, dt.getLength(), nm, cm);
                    }
                } catch (Exception e) {
                    println("  構造体 " + en.getKey() + " +" + Integer.toHexString(off) + ": " + e.getMessage());
                }
            }
            dtm.addDataType(s, DataTypeConflictHandler.REPLACE_HANDLER);
            n++;
        }
        return n;
    }
}
