import util.loader as loader

def run():
    nativeElements = loader.load_native_xls()

    loader.serialize_choosen_elements(nativeElements)

    #loader.deserialize_native()
