import pickle

file_path = ('./final_proj/web_app/static/l3e15eg8jby3frfw0fi0f5oeeo63datk/data.pkl')

with open(file_path, 'rb') as fp:
        data = pickle.load(fp)

print(data['url'])