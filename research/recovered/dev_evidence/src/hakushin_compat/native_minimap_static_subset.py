"""Bounded model of a saved Ghidra *subset* of original MiniMapWnd.

Evidence (existing decompile ZIP only):
  0x4DD8C0: separate 2D COLORREF grid, ceil cell spans, GDI rectangles.
  0x4DE330: already-transformed coordinates / 8, clamped overlay index;
            two overlay vertex color DWORD writes.
  0x4DE690: two mouse-drag slots are reset to the native sentinel.
  0x4DE410: mouse/camera effects exist; mapping is not proven here.
The color grid's producer, full transform, fog meaning, raster clipping,
battle runtime and user-visible parity are explicitly NOT reconstructed.
"""
from __future__ import annotations

from dataclasses import dataclass

NATIVE_RASTER_VA = 0x4DD8C0
NATIVE_OVERLAY_VA = 0x4DE330
NATIVE_DRAG_RESET_VA = 0x4DE690
NATIVE_INPUT_VA = 0x4DE410
NATIVE_NO_COORD = 0x80000008
MAX_CELLS = 1_000_000


class MiniMapContractUnknown(ValueError):
    """Outside the narrow native branch established from saved evidence."""


@dataclass(frozen=True, slots=True)
class DirectRgbColorGrid:
    """Caller-provided, row-major direct COLORREF values; not raw .map tags.

    Only Win32 direct RGB 0x00BBGGRR is accepted.  Palette-index / system
    COLORREF variants need separate original native verification.
    """
    rows: tuple[tuple[int, ...], ...]

    def __post_init__(self):
        if type(self.rows) is not tuple or not self.rows:
            raise MiniMapContractUnknown("nonempty tuple of rows required")
        width = len(self.rows[0]) if type(self.rows[0]) is tuple else 0
        if not width or width * len(self.rows) > MAX_CELLS:
            raise MiniMapContractUnknown("bounded positive grid shape required")
        for row in self.rows:
            if type(row) is not tuple or len(row) != width:
                raise MiniMapContractUnknown("all grid rows must be rectangular tuples")
            if any(type(v) is not int or not 0 <= v <= 0xFFFFFF for v in row):
                raise MiniMapContractUnknown("direct Win32 RGB COLORREF only")

    @property
    def columns(self) -> int:
        return len(self.rows[0])

    @property
    def row_count(self) -> int:
        return len(self.rows)

    def colorref(self, column: int, row: int) -> int:
        if (type(column) is not int or type(row) is not int
                or not 0 <= column < self.columns
                or not 0 <= row < self.row_count):
            raise MiniMapContractUnknown("grid indices outside validated source")
        return self.rows[row][column]


def direct_colorref_to_rgb(value: int) -> tuple[int, int, int]:
    """Interpret Win32 0x00BBGGRR only, never renderer alpha or palette bits."""
    if type(value) is not int or not 0 <= value <= 0xFFFFFF:
        raise MiniMapContractUnknown("unknown COLORREF variant")
    return value & 255, (value >> 8) & 255, (value >> 16) & 255


@dataclass(frozen=True, slots=True)
class NativeCellSpans:
    width_pixels: int
    height_pixels: int
    source_rows: int
    source_columns: int
    step_x: int
    step_y: int
    coordinate_transform_reconstructed: bool = False


def proven_ceil_cell_spans(
    color_grid: DirectRgbColorGrid, span_x: int, span_y: int
) -> NativeCellSpans:
    """0x4DD8C0 calls ceil helper 0x5B6ED0 on abs(span)/grid dims.

    x87/pixel placement & 0x4DCCB0 transformation are a SEPARATE barrier.
    No original screen origin or D3DX transform is inferred by this call.
    """
    if type(color_grid) is not DirectRgbColorGrid:
        raise MiniMapContractUnknown("typed source grid required")
    if (type(span_x) is not int or type(span_y) is not int
            or not 0 < abs(span_x) <= 8192
            or not 0 < abs(span_y) <= 8192):
        raise MiniMapContractUnknown("bounded nonzero display spans required")
    return NativeCellSpans(
        abs(span_x), abs(span_y), color_grid.row_count, color_grid.columns,
        (abs(span_x) + color_grid.columns - 1) // color_grid.columns,
        (abs(span_y) + color_grid.row_count - 1) // color_grid.row_count,
    )


@dataclass(frozen=True, slots=True)
class RelativeColorRectangle:
    """Relative axis-aligned study plan; not native D3DX screen coordinates."""
    column: int
    row: int
    local_left: int
    local_top: int
    local_right: int
    local_bottom: int
    source_colorref: int

    @property
    def direct_rgb(self) -> tuple[int, int, int]:
        return direct_colorref_to_rgb(self.source_colorref)


def synthetic_axis_aligned_rectangles(
    grid: DirectRgbColorGrid, spans: NativeCellSpans
) -> tuple[RelativeColorRectangle, ...]:
    """Display-agnostic rectangle list, only after explicit axis selection.

    Does not replicate 0x4DCCB0's origin/centering/matrix path or GDI clip.
    The final cells intentionally may extend beyond spans (ceil rectangle).
    """
    if type(grid) is not DirectRgbColorGrid or type(spans) is not NativeCellSpans:
        raise MiniMapContractUnknown("typed native scalar cells and spans required")
    if (grid.columns, grid.row_count) != (spans.source_columns, spans.source_rows):
        raise MiniMapContractUnknown("source color grid/spans mismatch")
    if (spans.coordinate_transform_reconstructed or spans.width_pixels <= 0
            or spans.height_pixels <= 0 or
            spans.step_x != (spans.width_pixels + grid.columns - 1)//grid.columns
            or spans.step_y != (spans.height_pixels + grid.row_count - 1)//grid.row_count):
        raise MiniMapContractUnknown("unsupported/forged native cell transform")
    return tuple(
        RelativeColorRectangle(column, row, column * spans.step_x,
                               row * spans.step_y, (column+1)*spans.step_x,
                               (row+1)*spans.step_y, grid.colorref(column,row))
        for row in range(grid.row_count) for column in range(grid.columns)
    )


@dataclass(frozen=True, slots=True)
class OverlayPatch:
    """0x4DE330: both corresponding vertex-color DWORD slots get this value."""
    overlay_column: int
    overlay_row: int
    linear_index: int
    vertex_color_dword: int
    same_value_written_to_two_vertices: bool = True
    fog_or_visibility_gameplay_meaning_verified: bool = False


def native_overlay_patch_for_transformed_coordinate(
    transformed_x: int, transformed_y: int,
    overlay_columns: int, overlay_rows: int, *,
    param3_nonzero: bool, stored_alpha_byte: int
) -> OverlayPatch:
    """ONLY for already-transformed integer positions from 0x4DE330.

    32-bit signed division by 8 truncates toward zero; then indices clamp.
    Native screen/world transform and caller visibility effects are unknown.
    """
    for name, value in (
        ("transformed_x", transformed_x), ("transformed_y", transformed_y)):
        if type(value) is not int or not -(1<<31) <= value < (1<<31):
            raise MiniMapContractUnknown(name + " must be raw signed int32")
    if (type(overlay_columns) is not int or type(overlay_rows) is not int
            or not 1 <= overlay_columns <= 4096
            or not 1 <= overlay_rows <= 4096
            or overlay_columns*overlay_rows > MAX_CELLS):
        raise MiniMapContractUnknown("bounded positive native overlay grid required")
    if (type(param3_nonzero) is not bool or type(stored_alpha_byte) is not int
            or not 0 <= stored_alpha_byte <= 255):
        raise MiniMapContractUnknown("native arg3 and alpha require exact types")

    def index(raw: int, limit: int) -> int:
        # C x86 expression (raw + ((raw>>31)&7)) >> 3, then clamp 0..N-1.
        truncated = raw//8 if raw >= 0 else -((-raw)//8)
        return max(0, min(limit-1, truncated))

    col = index(transformed_x, overlay_columns)
    row = index(transformed_y, overlay_rows)
    dword = 0 if param3_nonzero else stored_alpha_byte << 24
    return OverlayPatch(col, row, overlay_columns*row+col, dword)


@dataclass(frozen=True, slots=True)
class MiniMapDragReset:
    slot_168: int = NATIVE_NO_COORD
    slot_16c: int = NATIVE_NO_COORD
    input_command_verified: bool = False
    screen_transform_verified: bool = False


def reset_native_minimap_drag_slots() -> MiniMapDragReset:
    """The exact two stores in MiniMapWnd::vf16 (0x4DE690), nothing more."""
    return MiniMapDragReset()



# NEW 2026-10-11: 0x4DD8C0 overlay buffer topology only (saved Ghidra C).
# Caller-supplied grid size; no proof of original .map -> grid dimensions.
@dataclass(frozen=True, slots=True)
class NativeOverlayMeshTopology:
    """Two 0x18-byte vertex slots per 8-cell sampling-grid point.

    0x008A307C/80/84 are counters read from the saved 0x4DD8C0
    decompilation. This is not an actual fog/visibility shader model.
    """
    source_columns: int
    source_rows: int
    overlay_columns: int
    overlay_rows: int
    vertex_slot_count: int
    vertex_byte_stride: int = 0x18
    color_grid_producer_verified: bool = False
    vertex_screen_positions_verified: bool = False
    visual_blend_mode_verified: bool = False


def native_overlay_mesh_topology_from_grid_shape(
    source_columns: int, source_rows: int, *, flag_1eeee0_nonzero: bool
) -> NativeOverlayMeshTopology | None:
    """Local 0x4DD8C0 calculation, NOT original scene/color producer.

    +0x1EEEE0==0 skips the initialization branch in this function;
    it does not prove another owner destroyed existing overlay state.
    Source dimensions are validated even for the disabled branch.
    """
    if (type(source_columns) is not int or type(source_rows) is not int
            or type(flag_1eeee0_nonzero) is not bool
            or not 1 <= source_columns <= 8192
            or not 1 <= source_rows <= 8192
            or source_columns * source_rows > MAX_CELLS):
        raise MiniMapContractUnknown("unknown or oversized source grid shape")
    if not flag_1eeee0_nonzero:
        return None
    cols = (source_columns // 8) + 1
    rows = (source_rows // 8) + 1
    count = 2 * cols * rows
    return NativeOverlayMeshTopology(
        source_columns, source_rows, cols, rows, count)


def native_overlay_vertex_slot_pair(
    layout: NativeOverlayMeshTopology, column: int, row: int
) -> tuple[int, int]:
    """Saved decomp's 0x4DD8C0 serpentine row layout.

    Even rows advance from left to right; odd rows store grid cells in
    reverse order. The two 0x18-byte vertices stay adjacent for a cell.
    This is *buffer indexing*, not confirmed GPU primitive topology.
    """
    if type(layout) is not NativeOverlayMeshTopology:
        raise MiniMapContractUnknown("native overlay layout required")
    reference = native_overlay_mesh_topology_from_grid_shape(
        layout.source_columns, layout.source_rows, flag_1eeee0_nonzero=True)
    if layout != reference:
        raise MiniMapContractUnknown("layout fields do not match native counters")
    if (type(column) is not int or type(row) is not int
            or not 0 <= column < layout.overlay_columns
            or not 0 <= row < layout.overlay_rows):
        raise MiniMapContractUnknown("overlay vertex index outside mesh")
    c = column if row % 2 == 0 else layout.overlay_columns - 1 - column
    first = row * layout.overlay_columns * 2 + c * 2
    second = first + 1
    return first, second
