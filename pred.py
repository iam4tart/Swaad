import pandas as pd
import numpy as np
import sklearn
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
Ure = pd.read_csv("RAW_interactions.csv")
Re = pd.read_csv("RAW_recipes.csv")

def create_mat(df):
    N = len(df['user_id'].unique())
    M = len(df['recipe_id'].unique())
    user_map = dict(zip(np.unique(df['user_id']), list(range(N))))
    recipe_map = dict(zip(np.unique(df['recipe_id']), list(range(M))))
    user_inv_map = dict(zip(list(range(N)), np.unique(df['user_id'])))
    recipe_inv_map = dict(zip(list(range(M)), np.unique(df['recipe_id'])))
    
    user_idx = [user_map[i] for i in df['user_id']]
    recipe_idx = [recipe_map[i] for i in df['recipe_id']]
    
    X = csr_matrix((df["rating"], (recipe_idx, user_idx)), shape=(M, N))
      
    return X, user_map, recipe_map, user_inv_map, recipe_inv_map
X, user_map, recipe_map, user_inv_map, recipe_inv_map = create_mat(Ure)
def find_similar_recipes(recipe_id, X, k, metric='cosine', show_distance=False): 
    neighbour_ids = []
      
    recipe_ind = recipe_map[recipe_id]
    recipe_vec = X[recipe_ind]
    k+=1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    recipe_vec = recipe_vec.reshape(1,-1)
    neighbour = kNN.kneighbors(recipe_vec, return_distance=show_distance)
    for i in range(0,k):
        n = neighbour.item(i)
        neighbour_ids.append(recipe_inv_map[n])
    neighbour_ids.pop(0)
    return neighbour_ids
def dish_recommender(dish):
    dfund = pd.DataFrame(Re['name'],Re['id'])
    desr = pd.DataFrame(Re['description'],Re['id'])
    recipe_map_ni = dict(zip(Re['name'],Re['id']))
    
    Rdf = pd.DataFrame(Ure)
    n_rate = len(Ure)
    n_recipe = len(Ure['recipe_id'].unique())
    n_user = len(Ure['user_id'].unique())
    user_freq = Ure[['user_id', 'recipe_id']].groupby('user_id').count().reset_index()
    user_freq.columns = ['user_id', 'n_rate']
    mean_rat = Ure.groupby('recipe_id')[['rating']].mean()
    lower_rated = mean_rat['rating'].idxmin()
    Re.loc[Re['id'] == lower_rated]
    highest_rated = mean_rat['rating'].idxmax()
    Re.loc[Re['id']== highest_rated]
    recipe_stats = Ure.groupby('recipe_id')[['rating']].agg(['count', 'mean'])
    recipe_stats.columns = recipe_stats.columns.droplevel()

    desr_map = dict(zip(Re['id'],Re['description']))
    recipe_titles = dict(zip(Re['id'], Re['name']))
    dish_name = dish
    similar_dish = recipe_map_ni[dish_name]
    similar_ids = find_similar_recipes(similar_dish, X, k = 10)
    recipe_title = recipe_titles[similar_dish]
    print(f"Since you ate {recipe_title}")
    titles=[]
    description = []
   
    for i in similar_ids:
        titles.append(recipe_titles[i])
        description.append(desr_map[i])

    # print(description)

    return titles,description

# def jaccard(list1, list2):
#     intersection = len(list(set(list1).intersection(list2)))
#     union = (len(list1) + len(list2)) - intersection
#     return (intersection) / union
# d = pd.read_csv("indian_food.csv")

# d['ingredients'] = d['ingredients'].apply(lambda x: [str(i) for i in x.split(',')])
# df = pd.DataFrame(d)
# #Udf = df[['naam', 'ingredients', 'flavor_profile']].copy()
# def dish_ing(ing1,ing2,ing3):
#     InL=[]
#     InL.append(ing1)
#     InL.append(ing2)
#     InL.append(ing3)
#     Lsim = []
#     for row in range(0, len(df['ingredients'])):
#         a = jaccard(df.iloc[row]['ingredients'], InL)
#         Lsim.append(a)
#     max_s = max(Lsim)
#     idx1 = Lsim.index(max_s)
#     temp = Lsim[:]
#     temp.sort()
#     max2 = temp[len(temp)-2]
#     max3 = temp[len(temp)-3]
#     idx2 = Lsim.index(max2)
#     return [df.iloc[idx1]['name'],df.iloc[idx2]['name']]


def ingToDish(in1, in2, in3):
    df = pd.read_csv("indian_food.csv")
    df = pd.DataFrame(df)
    df.head()

    food_vocab = set()

    for ingredients in df['ingredients']:
        for food in ingredients.split(','):
        # we dont want any Capital character and dont want any spaces and want all unique food value in food_vocab, so below loop will make sure
            if food.strip().lower() not in food_vocab:
                food_vocab.add(food.strip().lower())

    ing_df = pd.DataFrame()

    for i, ingredients in enumerate(df['ingredients']):
        for food in ingredients.split(','):
            if food.strip().lower() in food_vocab:
                ing_df.loc[i, food.strip().lower()] = 1

    ing_df = ing_df.fillna(0)
    ing_df['name'] = df['name']

    User_il = [in1, in2, in3]
    # for i in range(0,3):
    #     User_in = input("Enter the ingridients: ")
    #     User_il.append(User_in)

    col = list(ing_df)

    l1 = []
    l2 = []
    l3 = []
    suml = []
    for k in range(0,255):
        su = 0
        for j in User_il:
            su += ing_df[j][k]
    
        suml.append(su)
    
        if(su == 1.0):
            l1.append(k)
        elif(su == 2.0):
            l2.append(k)
        elif(su==3.0):
            l3.append(k)

    ll = l1+l2+l3

    name1 = ing_df.iloc[ll[len(ll)-1]]['name']
    name2 = ing_df.iloc[ll[len(ll)-2]]['name']
    name3 = ing_df.iloc[ll[len(ll)-3]]['name']
    
    ingredients1 = df.iloc[ll[len(ll)-1]]['ingredients']
    ingredients2 = df.iloc[ll[len(ll)-2]]['ingredients']
    ingredients3 = df.iloc[ll[len(ll)-3]]['ingredients']
    
    print(name1, name2, name3)
    return([name1,name2,name3,ingredients1,ingredients2,ingredients3])
    
    