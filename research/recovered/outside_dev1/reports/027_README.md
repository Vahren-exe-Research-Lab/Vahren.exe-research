# フルスクリーンの説明表示その2（2026-11-01 Claude）
- 原因: フルスクリーンでは Direct3D が「D3DProxyWindow」という同じプロセスの窓をゲームの窓の上に置くため、「カーソルの下の一番上の窓がゲームか」の判定で常に弾いていた（hover_route reason=3 top_class=D3DProxyWindow）。
- 対策: 自プロセスの D3DProxyWindow だけは素通しで判定。
- 前の版: ..\\hoverfs_20261031
