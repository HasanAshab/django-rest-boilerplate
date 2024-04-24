def postprocess_components(result, generator, request, public):
    print(result['components']['schemas'].keys())
    
    return result