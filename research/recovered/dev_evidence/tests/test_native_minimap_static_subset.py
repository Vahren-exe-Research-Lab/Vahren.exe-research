"""Source-linked tests for an isolated MiniMapWnd native raster/overlay subset."""
import unittest
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from zipfile import ZipFile

from hakushin_compat.native_minimap_static_subset import (
    DirectRgbColorGrid, MiniMapContractUnknown, NATIVE_NO_COORD,
    NATIVE_RASTER_VA, NATIVE_OVERLAY_VA,
    direct_colorref_to_rgb, proven_ceil_cell_spans,
    synthetic_axis_aligned_rectangles,
    native_overlay_patch_for_transformed_coordinate,
    native_overlay_mesh_topology_from_grid_shape,
    native_overlay_vertex_slot_pair,
    reset_native_minimap_drag_slots,
)

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/"recovered_source"/"peer_script01_ghidra_named_decomp_20261011.zip"


class MiniMapNativeScalarTests(unittest.TestCase):
    @staticmethod
    def grid():
        return DirectRgbColorGrid((
            (0x0000FF,0x00FF00,0xFF0000),
            (0x000000,0x123456,0xFFFFFF),
        ))

    def test_source_grid_row_major_but_not_raw_map(self):
        grid=self.grid()
        self.assertEqual((grid.columns,grid.row_count),(3,2))
        self.assertEqual(grid.colorref(2,0),0xFF0000)
        self.assertEqual(grid.colorref(1,1),0x123456)

    def test_source_grid_refuses_negative_python_index_wraparound(self):
        grid=self.grid()
        for column,row in ((-1,0),(3,0),(0,-1),(0,2),(True,1),(0,False)):
            with self.subTest(column=column,row=row):
                with self.assertRaises(MiniMapContractUnknown):
                    grid.colorref(column,row)

    def test_win32_bgr_colorref_to_rgb_low_24_bits_only(self):
        self.assertEqual(direct_colorref_to_rgb(0x0000FF),(255,0,0))
        self.assertEqual(direct_colorref_to_rgb(0x00FF00),(0,255,0))
        self.assertEqual(direct_colorref_to_rgb(0xFF0000),(0,0,255))
        self.assertEqual(direct_colorref_to_rgb(0x123456),(0x56,0x34,0x12))

    def test_ceil_per_axis_not_floor(self):
        spans=proven_ceil_cell_spans(self.grid(),10,7)
        self.assertEqual((spans.step_x,spans.step_y),(4,4))
        self.assertEqual((spans.width_pixels,spans.height_pixels),(10,7))
        self.assertFalse(spans.coordinate_transform_reconstructed)

    def test_negative_display_spans_are_only_abs_scales(self):
        spans=proven_ceil_cell_spans(self.grid(),-10,-7)
        self.assertEqual((spans.step_x,spans.step_y),(4,4))
        self.assertFalse(spans.coordinate_transform_reconstructed)

    def test_forged_projection_metadata_fails_closed(self):
        grid=self.grid()
        spans=proven_ceil_cell_spans(grid,10,7)
        for illegal in (
            replace(spans,step_x=3),
            replace(spans,step_y=3),
            replace(spans,width_pixels=0),
            replace(spans,coordinate_transform_reconstructed=True),
        ):
            with self.subTest(illegal=illegal),self.assertRaises(MiniMapContractUnknown):
                synthetic_axis_aligned_rectangles(grid,illegal)

    def test_relative_cells_preserve_source_order_and_native_colorref(self):
        grid=self.grid()
        spans=proven_ceil_cell_spans(grid,10,7)
        cells=synthetic_axis_aligned_rectangles(grid,spans)
        self.assertEqual(len(cells),6)
        self.assertEqual((cells[0].column,cells[0].row),(0,0))
        self.assertEqual((cells[2].column,cells[2].row),(2,0))
        self.assertEqual((cells[3].column,cells[3].row),(0,1))
        self.assertEqual((cells[2].local_left,cells[2].local_right),(8,12))
        self.assertEqual((cells[-1].local_top,cells[-1].local_bottom),(4,8))
        self.assertEqual(cells[-1].direct_rgb,(255,255,255))

    def test_relative_rectangles_explicitly_exceed_native_span_when_ceil(self):
        grid=self.grid()
        cells=synthetic_axis_aligned_rectangles(
            grid,proven_ceil_cell_spans(grid,10,7))
        self.assertEqual(cells[2].local_right,12)
        self.assertEqual(cells[5].local_bottom,8)
        # Original GDI clip behavior cannot be inferred from these endpoints.
        self.assertGreater(cells[2].local_right,10)

    def test_ragged_empty_and_mutable_rows_fail_closed(self):
        bad=(
            (), ((1,2), (1,)), ([1,2],), ((1,2),[3,4]),
            ((True,),), ((-1,),), ((0x1000000,),), ((0.5,),),
        )
        for rows in bad:
            with self.subTest(rows=rows),self.assertRaises(MiniMapContractUnknown):
                DirectRgbColorGrid(rows)

    def test_non_direct_palette_or_alpha_bits_rejected(self):
        for value in (-1,0x80000001,0xFF000000,True,1.0):
            with self.subTest(value=value),self.assertRaises(MiniMapContractUnknown):
                direct_colorref_to_rgb(value)

    def test_invalid_spans_and_mixed_grid_shapes_refused(self):
        grid=self.grid()
        for width,height in ((0,4),(4,0),(8193,5),(True,5),(5,4.0)):
            with self.subTest(width=width,height=height):
                with self.assertRaises(MiniMapContractUnknown):
                    proven_ceil_cell_spans(grid,width,height)
        spans=proven_ceil_cell_spans(grid,9,6)
        wrong=DirectRgbColorGrid(((1,2),))
        with self.assertRaises(MiniMapContractUnknown):
            synthetic_axis_aligned_rectangles(wrong,spans)

    def test_overlay_divides_transformed_pixels_by_eight(self):
        fn=native_overlay_patch_for_transformed_coordinate
        results=[
            (0,0,(0,0,0)), (7,7,(0,0,0)), (8,0,(1,0,1)),
            (15,16,(1,2,13)), (48,15,(5,1,11)), (999,999,(5,3,23)),
            (-7,-8,(0,0,0)), (-100,100,(0,3,18)),
        ]
        for x,y,expected in results:
            with self.subTest(x=x,y=y):
                p=fn(x,y,6,4,param3_nonzero=True,stored_alpha_byte=255)
                self.assertEqual((p.overlay_column,p.overlay_row,p.linear_index),expected)
                self.assertEqual(p.vertex_color_dword,0)
                self.assertTrue(p.same_value_written_to_two_vertices)
                self.assertFalse(p.fog_or_visibility_gameplay_meaning_verified)

    def test_overlay_keeps_mask_byte_in_high_byte_only(self):
        fn=native_overlay_patch_for_transformed_coordinate
        self.assertEqual(
            fn(10,10,3,3,param3_nonzero=False,stored_alpha_byte=128).vertex_color_dword,
            0x80000000)
        self.assertEqual(
            fn(10,10,3,3,param3_nonzero=False,stored_alpha_byte=255).vertex_color_dword,
            0xFF000000)

    def test_overlay_native_index_bounded_and_exact(self):
        fn=native_overlay_patch_for_transformed_coordinate
        for dims in ((0,5),(4,0),(-1,2),(5000,1),(True,4),(1001,1001)):
            with self.subTest(dims=dims),self.assertRaises(MiniMapContractUnknown):
                fn(1,2,*dims,param3_nonzero=False,stored_alpha_byte=255)
        for x,y in ((2**31,0),(-(2**31)-1,0),(0,2**31)):
            with self.subTest(coords=(x,y)),self.assertRaises(MiniMapContractUnknown):
                fn(x,y,6,4,param3_nonzero=False,stored_alpha_byte=255)
        for alpha in (256,-1,True,2.0):
            with self.subTest(alpha=alpha),self.assertRaises(MiniMapContractUnknown):
                fn(1,2,6,4,param3_nonzero=False,stored_alpha_byte=alpha)
        with self.assertRaises(MiniMapContractUnknown):
            fn(1,2,6,4,param3_nonzero=1,stored_alpha_byte=50)

    def test_drag_reset_no_false_input_claim(self):
        reset=reset_native_minimap_drag_slots()
        self.assertEqual(reset.slot_168,NATIVE_NO_COORD)
        self.assertEqual(reset.slot_16c,NATIVE_NO_COORD)
        self.assertFalse(reset.input_command_verified)
        self.assertFalse(reset.screen_transform_verified)
        with self.assertRaises(FrozenInstanceError):
            reset.slot_168=0

    @unittest.skipUnless(ARCHIVE.is_file(),"saved named decompile unavailable")
    def test_vas_are_grounded_in_saved_native_source_not_photos(self):
        with ZipFile(ARCHIVE) as z:
            fname=next(n for n in z.namelist() if "decomp_004Dxxxx.c" in n)
            s=z.read(fname).decode("utf-8","replace")
        raster=s[s.find("/* ==== 0x004DD8C0 "):s.find("/* ==== 0x004DDCF0 ")]
        mask=s[s.find("/* ==== 0x004DE330 "):s.find("/* ==== 0x004DE410 ")]
        reset=s[s.find("/* ==== 0x004DE690 "):s.find("/* ==== 0x004DE6B0 ")]
        self.assertEqual(NATIVE_RASTER_VA,0x4DD8C0)
        self.assertEqual(NATIVE_OVERLAY_VA,0x4DE330)
        for text in ("0x1ef6b4","SetDCBrushColor","FillRect","FUN_005b6ed0"):
            self.assertIn(text,raster)
        for text in ("0x2397c","0x23980","0x23988","<< 0x18"):
            self.assertIn(text,mask)
        self.assertEqual(reset.count("0x80000008"),2)
        self.assertIn("MiniMapWnd__vf16",reset)


class NativeOverlayMeshTopologyTests(unittest.TestCase):
    def test_grid_samples_floor_div8_plus_one_not_ceil(self):
        fn = native_overlay_mesh_topology_from_grid_shape
        for width, expected in ((1,1), (7,1), (8,2), (9,2),
                                (15,2), (16,3), (17,3), (110,14)):
            with self.subTest(width=width):
                plan=fn(width,9,flag_1eeee0_nonzero=True)
                self.assertEqual(plan.overlay_columns,expected)
                self.assertEqual(plan.overlay_rows,2)
                self.assertEqual(plan.vertex_slot_count,2*expected*2)
                self.assertEqual(plan.vertex_byte_stride,0x18)
                self.assertFalse(plan.color_grid_producer_verified)

    def test_110_by_110_shape_is_only_a_synthetic_example(self):
        plan=native_overlay_mesh_topology_from_grid_shape(
            110,110,flag_1eeee0_nonzero=True)
        self.assertEqual((plan.overlay_columns,plan.overlay_rows),(14,14))
        self.assertEqual(plan.vertex_slot_count,392)
        self.assertFalse(plan.vertex_screen_positions_verified)
        self.assertFalse(plan.visual_blend_mode_verified)

    def test_disabled_flag_does_not_assert_cleared_overlay(self):
        self.assertIsNone(native_overlay_mesh_topology_from_grid_shape(
            110,110,flag_1eeee0_nonzero=False))
        with self.assertRaises(MiniMapContractUnknown):
            native_overlay_mesh_topology_from_grid_shape(
                10,10,flag_1eeee0_nonzero=0)
        # None = branch not taken, not a claim about previous-frame teardown.

    def test_serpentine_odd_rows_reverse_cell_slot_order(self):
        plan=native_overlay_mesh_topology_from_grid_shape(
            17,9,flag_1eeee0_nonzero=True)
        self.assertEqual((plan.overlay_columns,plan.overlay_rows,
                          plan.vertex_slot_count),(3,2,12))
        pairs=[
            (0,0,(0,1)), (1,0,(2,3)), (2,0,(4,5)),
            (0,1,(10,11)), (1,1,(8,9)), (2,1,(6,7)),
        ]
        for col,row,expected in pairs:
            with self.subTest(col=col,row=row):
                self.assertEqual(native_overlay_vertex_slot_pair(plan,col,row),
                                 expected)
        all_slots=sorted(s for c,r,_ in pairs
                         for s in native_overlay_vertex_slot_pair(plan,c,r))
        self.assertEqual(all_slots,list(range(plan.vertex_slot_count)))

    def test_third_row_returns_left_to_right(self):
        plan=native_overlay_mesh_topology_from_grid_shape(
            17,17,flag_1eeee0_nonzero=True)
        self.assertEqual(native_overlay_vertex_slot_pair(plan,0,2),(12,13))
        self.assertEqual(native_overlay_vertex_slot_pair(plan,2,2),(16,17))
        self.assertEqual(native_overlay_vertex_slot_pair(plan,0,1),(10,11))

    def test_rejects_unsafe_shape_and_python_bool(self):
        cases=((0,2),(-1,10),(2,0),(1,-3),(True,2),
               (3,False),(8193,1),(1001,1000))
        for width,height in cases:
            with self.subTest(shape=(width,height)):
                with self.assertRaises(MiniMapContractUnknown):
                    native_overlay_mesh_topology_from_grid_shape(
                        width,height,flag_1eeee0_nonzero=True)

    def test_rejects_forged_layout_and_invalid_slot_index(self):
        plan=native_overlay_mesh_topology_from_grid_shape(
            17,9,flag_1eeee0_nonzero=True)
        for forged in (replace(plan,overlay_columns=4),
                       replace(plan,overlay_rows=8),
                       replace(plan,vertex_slot_count=500),
                       replace(plan,vertex_byte_stride=16),
                       replace(plan,visual_blend_mode_verified=True)):
            with self.subTest(forged=forged):
                with self.assertRaises(MiniMapContractUnknown):
                    native_overlay_vertex_slot_pair(forged,0,0)
        for col,row in ((-1,0),(3,0),(0,2),(0,-1),(False,0),(0,True)):
            with self.subTest(index=(col,row)):
                with self.assertRaises(MiniMapContractUnknown):
                    native_overlay_vertex_slot_pair(plan,col,row)

    @unittest.skipUnless(ARCHIVE.is_file(),"saved Ghidra C archive absent")
    def test_saved_assembly_surrogate_guards_mesh_branch(self):
        with ZipFile(ARCHIVE) as z:
            name=next(n for n in z.namelist() if "decomp_004Dxxxx.c" in n)
            s=z.read(name).decode("utf-8","replace")
        start=s.find("/* ==== 0x004DD8C0 ")
        stop=s.find("/* ==== ",start+10)
        self.assertGreater(start,0)
        body=s[start:stop]
        for literal in ("0x1ef6b4", "0x1eeee0", "0x1eee4c",
                        "DAT_008a307c", "DAT_008a3080", "DAT_008a3084",
                        "DAT_008a3080 * DAT_008a307c * 2",
                        "uStack_28 = uVar5 & 1",
                        "iVar8 + iStack_30 * -2",
                        "iVar9 = iVar9 * 0x18"):
            with self.subTest(literal=literal):
                self.assertIn(literal,body)

    @unittest.skipUnless(ARCHIVE.is_file(),"saved Ghidra C archive absent")
    def test_saved_c_corpus_has_reader_but_no_direct_producer_xref(self):
        # Direct syntax search over this fixed ZIP, NOT proof the EXE has no
        # writer. Indirect base pointers and omitted disassembly remain.
        with ZipFile(ARCHIVE) as z:
            refs=[]
            for name in z.namelist():
                if not name.endswith(".c"):
                    continue
                s=z.read(name).decode("utf-8","replace")
                n=s.lower().count("0x1ef6b4")
                if n:
                    refs.append((name.rsplit("/",1)[-1],n))
        self.assertEqual(refs,[("decomp_004Dxxxx.c",1)])


if __name__=="__main__":
    unittest.main()
