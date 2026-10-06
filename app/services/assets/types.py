from io import BytesIO

type AssetDirectory = dict[str, AssetDirectory | BytesIO]
