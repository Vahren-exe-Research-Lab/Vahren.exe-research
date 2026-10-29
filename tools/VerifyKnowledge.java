// @category Hakushin
// Read-only verification of knowledge labels in an isolated analysis project.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.data.CategoryPath;
import ghidra.program.model.data.DataType;

public class VerifyKnowledge extends GhidraScript {
    @Override public void run() throws Exception {
        long[] addresses = {0x0048D6A0L, 0x00550E70L, 0x0054E7B0L,
            0x0057B870L, 0x00460000L, 0x005559B0L, 0x00597960L};
        int found = 0;
        for (long value : addresses) {
            Address a=toAddr(value);
            Function f = getFunctionAt(a);
            String name = f==null?"MISSING":f.getName();
            String end = f==null?"NA":f.getBody().getMaxAddress().toString();
            String plate=getPlateComment(a);
            boolean kb=plate!=null && plate.contains("【KB】");
            println(String.format("KB_VERIFY va=0x%08X name=%s end=%s kb_comment=%s",
               value,name,end,kb));
            if (f!=null && kb) found++;
        }
        Address code=toAddr(0x00419938L);
        ghidra.program.model.symbol.Symbol codeSymbol =
            currentProgram.getSymbolTable().getPrimarySymbol(code);
        String codeComment=getPreComment(code);
        println("KB_VERIFY code_419938_label="+
            (codeSymbol==null?"MISSING":codeSymbol.getName())+
            " comment="+(codeComment!=null && codeComment.contains("【KB】")));
        Address ret=toAddr(0x0048EA5AL);
        int opcode=currentProgram.getMemory().getByte(ret) & 0xff;
        println(String.format("KB_VERIFY battle_ret_opcode=0x%02X expected_C3=%s",
              opcode,opcode==0xC3));
        DataType dt=currentProgram.getDataTypeManager()
          .getDataType(new CategoryPath("/Hakushin"),"UnitDef");
        println("KB_VERIFY UnitDef="+(dt==null?"MISSING":dt.getName()));
        println("KB_VERIFY named_and_commented="+found+"/"+addresses.length);
    }
}
