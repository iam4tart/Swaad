from flask import Flask,render_template,request,redirect,flash 
from pandas import *
import pred as p
app=Flask(__name__)

@app.route("/")
def hello():
    # populating dish and description dropdown
    datar = read_csv("recipe_names.csv")
    list2 = datar['name'].tolist()
    list1=[]
    for i in list2:
        tempr={}
        tempr['name']=i
        list1.append(tempr)
    recipe_list = list1[:200]
    
    # populating ingredient dropdown
    datai = read_csv("ingredient_names.csv")
    list4 = datai['name'].tolist()
    list3=[]
    for j in list4:
        tempi={}
        tempi['name']=j
        list3.append(tempi)
    ingredient_list = list3

    
    return render_template("index.html",items_recipe = recipe_list, items_ingredient = ingredient_list)

@app.route("/recipe",methods=["GET","POST"])
def submit():
    if request.method=="POST":
        
        if request.form.get('action') == "varrec":
            
            dish=request.form.get('dish')
        
            dish_pred=p.dish_recommender(dish)
            print(dish_pred)
            most = dish_pred[0][0].title()
            most_desc = dish_pred[1][0]
            sim_2 = dish_pred[0][1].title()
            sim_2_desc = dish_pred[1][1]
            sim_3 = dish_pred[0][2].title()
            sim_3_desc = dish_pred[1][2]
            sim_4 = dish_pred[0][3].title()
            sim_4_desc = dish_pred[1][3] 
            
            sim_5 = dish_pred[0][4]
            sim_5_desc = dish_pred[1][4]
            return render_template("sub.html",most=most, sim_2=sim_2, sim_3=sim_3, sim_4=sim_4, sim_5=sim_5, most_desc=most_desc, sim_2_desc=sim_2_desc, sim_3_desc=sim_3_desc, sim_4_desc=sim_4_desc, sim_5_desc=sim_5_desc)
        
        elif request.form.get('action') == "varing":

            ing1=request.form["ing1"]
            ing2=request.form["ing2"]
            ing3=request.form["ing3"]
            
            dishes=p.ingToDish(ing1,ing2,ing3)
            
            return render_template("mel.html",m=dishes[0],n=dishes[1],o=dishes[2], x=dishes[3], y=dishes[4], z=dishes[5])

        else:
            print("breaking out")
            return redirect('/')

if __name__=="__main__":
    app.run()
