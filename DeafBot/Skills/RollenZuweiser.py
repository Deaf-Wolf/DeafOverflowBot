import discord

class RoleZuweiser:
    def __init__(self):
        self.role_message_id = None  # Add this attribute
        pass

    async def send_role_message(self, channel):
        print("Sending role message")
        message = await channel.send('What Role do you want')
        self.role_message_id = message.id  # Store the message ID
        # Add reactions
        await message.add_reaction('🔵')
        await message.add_reaction('🔴')

    async def process_reaction(self, reaction, user):
        if reaction.message.id != self.role_message_id:
            return  # Return if the reaction is not on the role message

        print(f"Reaction processed: {reaction.emoji} by {user.name}")

        # Process the reaction and assign roles based on the chosen emoji
        if str(reaction.emoji) == '🔵':
            role_id = 1121168953536958575
            success_message = 'You have been assigned the Blue Role!'
        elif str(reaction.emoji) == '🔴':
            role_id = 1121169012504674406
            success_message = 'You have been assigned the Red Role!'
        else:
            return

        guild = reaction.message.guild
        role = guild.get_role(role_id)
        member = guild.get_member(user.id)

        if role and member:
            await member.add_roles(role)
            print(f"Role assigned: {role.name} to {member.name}")
            await user.send(success_message)
