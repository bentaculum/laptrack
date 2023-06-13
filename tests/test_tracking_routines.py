import networkx as nx
import numpy as np

from laptrack._tracking import _get_segment_df


def test_get_segment_df() -> None:
    test_tree = nx.Graph()
    test_tree.add_edges_from(
        [
            ((0, 0), (1, 0)),
            ((1, 0), (2, 0)),
            ((2, 0), (3, 0)),
            ((3, 0), (4, 0)),
            ((2, 1), (3, 1)),
            ((2, 2), (3, 2)),
            ((3, 2), (4, 2)),
        ]
    )

    test_coords = [
        np.array([[1.0, 1.0]]),
        np.array([[2.0, 2.0], [2.1, 2.1]]),
        np.array([[3.0, 3.0], [3.1, 3.1], [3.2, 3.2]]),
        np.array([[4.0, 4.0], [4.1, 4.1], [4.2, 4.2]]),
        np.array([[5.0, 5.0], [5.1, 5.1], [5.2, 5.2]]),
    ]

    expected_segment_dfs = [
        ({(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)}, 0, 0, 4, 0, (1.0, 1.0), (5.0, 5.0)),
        (
            {
                (2, 1),
                (3, 1),
            },
            2,
            1,
            3,
            1,
            (3.1, 3.1),
            (4.1, 4.1),
        ),
        ({(2, 2), (3, 2), (4, 2)}, 2, 2, 4, 2, (3.2, 3.2), (5.2, 5.2)),
    ]

    segment_df = _get_segment_df(test_coords, test_tree)

    segment_df_set = []
    for i, row in segment_df.iterrows():
        segment_df_set.append(
            (
                set(row["segment"]),
                row["first_frame"],
                row["first_index"],
                row["last_frame"],
                row["last_index"],
                tuple(row["first_frame_coords"]),
                tuple(row["last_frame_coords"]),
            )
        )
    for s in segment_df_set:
        matched = False
        for s1 in expected_segment_dfs:
            if s1 == s:
                matched = True
        assert matched
