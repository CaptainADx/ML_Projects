import google.generativeai as genai

# Paste your API key here
genai.configure(api_key="AIzaSyAGv6xkj8LHGNGFEvx-VsVVOT_FB1ly_Vg")

# List all available models
for model in genai.list_models():
    print(model.name)
