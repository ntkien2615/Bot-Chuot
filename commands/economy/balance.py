import discord
from discord.ext import commands
from discord import app_commands
import mysql.connector  # Import the MySQL connector library

# Replace these with your actual connection details
MYSQL_HOST = "sql12.freesqldatabase.com"
MYSQL_USER = "sql12725224"
MYSQL_PASSWORD = "bN1exXNWYp"
MYSQL_DATABASE = "bot_chuot"

class Balance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Checks your account balance.")
    async def balance(self, interaction: discord.Interaction):
        user_id = interaction.user.id  # Get the user's ID from Discord

        try:
            # Connect to the MySQL database
            mydb = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE
            )
            mycursor = mydb.cursor()

            # Execute the SQL query to retrieve the balance
            sql = "SELECT coin FROM bot_chuot WHERE user_id = %s"
            val = (user_id,)
            mycursor.execute(sql, val)

            # Fetch the balance result
            myresult = mycursor.fetchone()

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
        finally:
            # Close the database connection (if successfully established)
            if mydb:
                mycursor.close()
                mydb.close()

async def setup(bot):
    await bot.add_cog(Balance(bot))