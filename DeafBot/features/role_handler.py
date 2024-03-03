# features/role_handler.py
from discord.ui import Button, View

class RoleCommandHandler:
    
    
    @staticmethod
    async def show_roles(message):
        roles = ', \n'.join([role.name for role in message.guild.roles if role.name != "@everyone" and role.name != "DeafBot"])
        await message.channel.send(f"Dieser Server hat die Rollen:\n{roles}")

        # Creates a button for each role
        view = View()
        server_roles = [role for role in message.guild.roles if role.name != "@everyone" and role.name != "DeafBot"]

        # Checks if Server has Roles
        if not server_roles:
            await message.channel.send(f"Keine Rollen zum Hinzufügen!")
        else:
            for role in server_roles:
                view.add_item(Button(label=role.name, custom_id=f"add_{role.id}"))
            await message.channel.send("Klicken Sie auf eine Schaltfläche, um eine Rolle hinzuzufügen.", view=view)


    @staticmethod
    async def remove_roles(message):
         #List roles of the user
        roles = ', \n'.join([role.name for role in message.author.roles if role.name != "@everyone" and role.name != "DeafBot"])
        await message.channel.send(f"{message.author.name} hat die Rollen:\n{roles}")

        #Creates a button for each role
        view = View()
        user_roles = [role for role in message.author.roles if role.name != "@everyone" and role.name != "DeafBot"]

        #Checks if user has a role or not
        if not user_roles:
            await message.channel.send(f"{message.author.name} hat keine Rollen HHAHAHAHA")
        else:
            for role in user_roles:
                view.add_item(Button(label=f"Entferne {role.name}", custom_id=f"remove_{role.id}"))
            await message.channel.send("Klicken Sie auf eine Schaltfläche, um eine Rolle zu entfernen.", view=view)
