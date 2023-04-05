import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="PASSWORD",
  database="calory_db",
  port="3006" # change to the correct port number
)



def sign_up():
    # prompt user for input
    userid = input("Enter email id: ")
    pin = int(input("Set a pin: "))
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (M/F): ")
    height = int(input("Enter your height in cm: "))
    weight = int(input("Enter your weight in kg: "))
    goal = input("What is your goal? (L/G/M): " )
    print()
    print("WELCOME ", name," !!!")
    PAL = workoutlevels()
    BMR = maintainence(gender, weight, height, age, PAL)
    store_users(userid, pin, name, age, gender, height, weight, goal)
    if goal == "L":
        Lose(BMR, weight)
    elif goal == "M":
            Maintain(BMR)        
    else:
           Gain(BMR, weight)
    return userid
           
def log_in():
    userid = input("Enter your registered email id: ")
    pin = int(input("Enter your pin: "))
# Prepare a SQL query to check if the user_id and pin combination exists
    query = "SELECT * FROM users WHERE userid = %s AND pin = %s"
    values = (userid, pin)

# Execute the query and retrieve the results
    mycursor = mydb.cursor()
    mycursor.execute(query, values)
    result = mycursor.fetchone()

# Check if a row was returned
    if result:
        print("WELCOME BACK")
    else:
        print("Sorry, user does not exist!!!")
    main()
        

def MENU(user_id):
    print("What would you like to do today?: \n")
    print("1. Log in food \n")
    print("2. Log in exercise \n")
    print("3. Review my day \n")
    print("4. Exit \n")
    ans=int(input("Enter choice: "))
    if ans == 1:
        NUTRITION(ans,user_id)
    elif ans == 2:
        EXERCISE(ans,user_id)
    elif ans== 3:
        REVIEW_TODAY()
    else:
        exit()
        
    
    
    
def store_users(userid, pin, name, age, gender, height, weight, goal):
    # create cursor to execute SQL queries
    mycursor = mydb.cursor()
    # insert data into "users" table
    sql = "INSERT INTO users (userid, pin, name, age, gender, height, weight, goal) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (userid, pin, name, age, gender, height, weight, goal)
    mycursor.execute(sql, val)

    # commit changes to the database
    mydb.commit()
    print()

def maintainence(gender, weight, height, age, PAL):
    #calculates maintainence calories based on input
    if gender == "M":
        BMR = (10 * weight) + (6.25 * height * 100) - (5 * age) + 5
    else:
        BMR = (10 * weight) + (6.25 * height * 100) - (5 * age) - 161
    CALORIE_INTAKE = BMR*PAL
    return CALORIE_INTAKE
    print()
    print("Your calorie intake per day must be around", int(CALORIE_INTAKE),"in order to maintain your current weight.")
    

def workoutlevels():
    print("What are your activity levels like: \n")
    print("1. Little / No Exercise")
    print("2. Light Exercise 1-2 times/week")
    print("3. Moderate Exercise 2-3 times/week")
    print("4. Hard Exercise  3-5 times/week")
    print("5. Physical Job 6-7 times/week")
    print("6. Professional Athlete")
    print("_______________________________________________________________")

    workout = int(input("Enter your selection (1, 2, 3, 4, 5 or 6): "))
    if workout == 1:
        PAL = 1
    elif workout == 2:
        PAL = 1.4
    elif workout == 3:
        PAL = 1.6
    elif workout == 4:
        PAL = 1.75
    elif workout == 5:
        PAL = 2
    else:
        PAL = 2.4
    return(PAL)
    

def Lose(CALORIE_INTAKE, weight):
    print("In order to lose weight, you must be in a calorie deficit.\n")
    print("_______________________________________________________________")
    print("What are your weekly weight loss goals?\n")
    print("1. 0.25 kg/week")
    print("2. 0.50 kg/week")
    print("3. 0.75 kg/week")
    print("4. 1 kg/week\n")
    print("_______________________________________________________________")
    weekly_goals = int(input("Enter your selection (1, 2, 3 or 4): "))
    print()
    ideal_weight=int(input("what is your ideal weight? "))
    if weekly_goals == 1:
        CALORIE_INTAKE-= 275
        days = ((weight - ideal_weight)*1100*7*7)/1925
    if weekly_goals == 2:
        CALORIE_INTAKE-= 550
        days = ((weight - ideal_weight)*1100*7*7)/3350
    if weekly_goals == 3:
        CALORIE_INTAKE-= 825
        days = ((weight - ideal_weight)*1100*7*7)/5775
    if weekly_goals == 4:
        CALORIE_INTAKE-= 1100
        days = ((weight - ideal_weight)*1100*7*7)/7700
    print("Your daily calorie intake according to your goals should be approximately ", CALORIE_INTAKE,".")
    print("You will achieve your ideal weight in", int(days)," days")
    

def Gain(CALORIE_INTAKE, weight):
    print("In order to gain weight, you must be in a calorie surplus.\n")
    print("To gain weight safely, focus on eating more nutrient-dense foods and living an overall healthy lifestyle that involves exercising, getting enough sleep, and reducing stress, if you can.")
    print("_______________________________________________________________")
    print("What are your weekly weight gain goals?\n")
    print("1. 0.25 kg/week")
    print("2. 0.50 kg/week")
    print("3. 0.75 kg/week")
    print("4. 1 kg/week\n")
    print("_______________________________________________________________")
    weekly_goals = int(input("Enter your selection (1, 2, 3 or 4): "))
    print()
    ideal_weight=int(input("what is your ideal weight? "))
    if weekly_goals == 1:
        CALORIE_INTAKE+= 275
        days = ((ideal_weight - weight)*1100*7*7)/1925
    if weekly_goals == 2:
        CALORIE_INTAKE+= 550
        days = ((ideal_weight - weight)*1100*7*7)/3350
    if weekly_goals == 3:
        CALORIE_INTAKE+= 825
        days = ((ideal_weight - weight)*1100*7*7)/5775
    if weekly_goals == 4:
        CALORIE_INTAKE+= 1100
        days = ((ideal_weight - weight)*1100*7*7)/7700
    print("Your daily calorie intake according to your goals should be approximately ", CALORIE_INTAKE,".")
    print("You will achieve your ideal weight in", abs(int(days))," days")
    
def Maintain(CALORIE_INTAKE):
    print("In order to maintain weight, you must consume your daily maintainence calories of", int(CALORIE_INTAKE))
    
def NUTRITION(ans,user_id):
    while ans == 1:
        print("The best way to reach your goals is to keep track of what is going inside your body")
        print("Track your meals on the daily.")
        food_name = input("Enter food name: ")
        calories = int(input("Enter calories: "))
        protein = int(input("Enter protein: "))
        fat = int(input("Enter fat: "))
        carbs = int(input("Enter carbs: "))
    
        # create cursor to execute SQL queries
        mycursor = mydb.cursor()
        # insert data into "nutritions" table
        sql = "INSERT INTO nutritions (user_id, food_name, calories, protein, fat, carbs) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (user_id, food_name, calories, protein, fat, carbs)
        mycursor.execute(sql, val)
        # commit changes to the database
        mydb.commit()
        print()
        
        print("Check out the nutritional values for the food you have consumed!")
        print()
        # Create a list of labels for the x-axis
        labels = ['Calories', 'Protein', 'Fat', 'Carbs']

        # Create a list of data for the y-axis
        data = [calories, protein, fat, carbs]

        # Create a bar chart
        plt.bar(labels, data)

        # Add a title and axis labels
        plt.title('Nutritional Information for Food Item')
        plt.xlabel('Nutrient')
        plt.ylabel('Amount (grams or calories)')

        # Show the plot
        plt.show()
        print("Would you like to:")
        print("1. Log more")
        print("2. Return to Menu")
        ans = int(input("Enter your choice: "))
    else:
        MENU(user_id)
    
    
    
    
def EXERCISE(ans,user_id):
    while ans == 2:
        print("Exercise is a celebration of what your body can do, not punishment for what you ate. \n")
        print("Log your exercise now.")
        workout = input("Enter exercise name: ")
        time = int(input("How much time did you spend on the activity in minutes?: "))
        calories_burnt = int(input("How many calories did you burn? : "))
        
        # create cursor to execute SQL queries
        mycursor = mydb.cursor()
        # insert data into "exercise" table
        sql = "INSERT INTO exercise (user_id, workout, time, calories_burnt) VALUES (%s, %s, %s, %s)"
        val = (user_id, workout, time, calories_burnt)
        mycursor.execute(sql, val)

        # commit changes to the database
        mydb.commit()
        print()
        print("Would you like to:")
        print("1. Return to Menu")
        print("2. Log more")
        ans = int(input("Enter your choice: "))
    else:
        MENU(user_id)
        
def REVIEW_TODAY():
    
    from datetime import date

# Get today's date
    today = date.today()

# Prepare a SQL query to get the nutrition data for today
    query = "SELECT SUM(calories), SUM(protein), SUM(fat), SUM(carbs) FROM nutritions WHERE date = %s"
    values = (today,)

# Execute the query and retrieve the results
    mycursor = mydb.cursor()
    mycursor.execute(query, values)
    result = mycursor.fetchall()[0]

# Define the labels for the pie chart
    labels = ['Calories', 'Protein', 'Fat', 'Carbs']

# Define the values for the pie chart
    values = [result[0], result[1], result[2], result[3]]

# Define the colors for the pie chart
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

# Create the pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(values, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')

# Show the pie chart
    plt.show()

# Prepare a SQL query to get the exercise data for today
    query = "SELECT workout, SUM(calories_burnt) FROM exercise WHERE date = %s GROUP BY workout"
    values = (today,)

# Execute the query and retrieve the results
    mycursor = mydb.cursor()
    mycursor.execute(query, values)
    results = mycursor.fetchall()

# Define the labels for the bar chart
    labels = [result[0] for result in results]

# Define the values for the bar chart
    values = [result[1] for result in results]

# Create the bar chart
    fig, ax = plt.subplots()
    ax.bar(labels, values)

# Set the title and axis labels
    ax.set_title('Exercise Calories Burned Today')
    ax.set_xlabel('Exercise')
    ax.set_ylabel('Calories Burned')

# Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

# Show the bar chart
    plt.show()
        
def exit() :
    
    print("Thank you for using Calory! Hope to see you back soon!")

def main():
     
    print()
    print("WELCOME!!!")
    print("Would you like to:")
    print("1. SIGN UP")
    print("2. LOG IN")
    print("3. Exit")
    choice = int(input("Enter choice: "))
    if choice == 1:
        user_id = sign_up()
        MENU(user_id)
    elif choice == 2:
        user_id = log_in()
        MENU(user_id)
    else:
        exit()
        
print(""" 
     +--------+
     | CALORY | 
     +--------+
     +------------------------------------------------+
     | HERE TO HELP YOU REACH YOUR GOALS SUSTAINIBLY |
     +------------------------------------------------+
     +-----------------------------------------+
     | HELP US HELP YOU CUSTOMISE YOUR JOURNEY |
     +-----------------------------------------+
     """)
     
     
main()
    
    
    
