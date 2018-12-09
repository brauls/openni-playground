"""entry point
"""

if __name__ == '__main__':
    from argparse import ArgumentParser

    PARSER = ArgumentParser()
    PARSER.add_argument(
        "stream_type",
        choices=["rgb", "depth", "ir"],
        help="select the type of stream video to be displayed"
    )
    ARGS = PARSER.parse_args()

    STREAM_TYPE = ARGS.stream_type
    if STREAM_TYPE == "rgb":
        from examples.rgb_stream import show_rgb_viewer
        show_rgb_viewer()
    elif STREAM_TYPE == "depth":
        from examples.depth_stream import show_depth_viewer
        show_depth_viewer()
    elif STREAM_TYPE == "ir":
        from examples.ir_stream import show_ir_viewer
        show_ir_viewer()
