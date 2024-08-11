import discord
from discord.ext import commands
from discord import app_commands
import mysql.connector  # Import the MySQL connector library

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Checks your account balance.")
    async def balance(self, interaction: discord.Interaction):
        user_id = interaction.user.id  # Get the user's ID from Discord

        try:
            # Connect to the MySQL database
            mydb = mysql.connector.connect(
                host= "sql12.freesqldatabase.com",
                user= "sql12725224",
                password= "bN1exXNWYp",
                database= "sql12725224"
            )
            mycursor = mydb.cursor()

            # Execute the SQL query to retrieve the balance
            sql = "SELECT coin FROM bot_chuot WHERE user_id = %s"
            val = (user_id,)
            mycursor.execute(sql, val)

            # Fetch the balance result
            myresult = mycursor.fetchone()

            mycursor.close()
            mydb.close()

            if myresult:
                balance = myresult[0]
                await interaction.response.send_message(f"Your current balance is: {balance} coin")  # Include the coin unit
            else:
                # User not found, add them to the table with initial balance
                sql = "INSERT INTO your_table (user_id, coin) VALUES (%s, %s)"
                val = (user_id, 10)  # Initial balance of 10
                mycursor.execute(sql, val)
                mydb.commit()  # Commit the insertion
                await interaction.response.send_message(f"Welcome! Your starting balance is: 10 coin")
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            await interaction.response.send_message("An error occurred while checking your balance. Please try again later.")
        

async def setup(bot):
    await bot.add_cog(Balance(bot))