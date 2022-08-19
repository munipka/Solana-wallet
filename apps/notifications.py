import asyncio
from apps.database import get_users_list, load_balance_db, update_balance_db
from apps.wallet import get_balance


async def notifications(bot):
    """send notification to user when the funds were received to the account"""
    users_list = await get_users_list()
    for user in users_list:
        new_balance = await get_balance(int(user[0]))
        old_balance = await load_balance_db(int(user[0]))
        if float(new_balance['balance']) > float(old_balance[0][0]):
            text = 'На Ваш кошелек поступило ' + str(float(new_balance['balance'])-float(old_balance[0][0])) + ' SOL'
            await bot.send_message(chat_id=int(user[0]), text=text)
            await update_balance_db((int(user[0])), float(new_balance['balance']))
    await asyncio.sleep(30)
    await notifications(bot)



