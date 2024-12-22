import asyncio
import traceback
from typing import Optional, Union, List

from asyncpg import UniqueViolationError
from sqlalchemy import and_, case
from gino import Gino
from models.schemas.team import TeamSchema
from models.schemas.user import UserSchema
from models.schemas.message import MessageSchema
from models.schemas.settings import SettingSchema
from models.schemas.pays import PaySchema
from models.schemas.mailing import MailingSchema
from models.schemas.promos import PromosSchema
from models.schemas.events import EventsSchema
from models.schemas.third import ThirdSchema
from models.schemas.second import SecondSchema
from models.schemas.first import FirstShema
from models.schemas.recent import RecentShema




class DbRecent:
    def __init__(self, user_id: Optional[int] = None, state: Optional[str] = '0', username: Optional[str] = 'Не указано'):
        self.user_id = user_id
        self.state = state
        self.username = username
        
    async def add(self):
        try:
            recent = RecentShema(user_id=self.user_id, state = self.state, username = self.username)
            return await recent.create()
        except UniqueViolationError:
            return False
       #не рабочая
    async def check(self):
        try:
            if self.user_id:
                try:
                    d = await RecentShema.query.where(RecentShema.user_id == self.user_id).gino.all()
                    if len(d) != None:
                        return 2
                    else:
                        return 1
                except:
                    return 1
            else:
                return 1 
        except Exception:
            return 0   
       
    async def select_recent(self):
     #   print(self.user_id)
        try: 
            return await RecentShema.query.where(RecentShema.user_id == self.user_id).gino.first()
        except Exception:
            return False


        
    
    async def select_etap(self, etap: str):
        print(await RecentShema.query.where(RecentShema.state == etap).gino.all())
        try:
           return await RecentShema.query.where(RecentShema.state == etap).gino.all()
        except Exception:
            return False
    
    async def select_user(self, id: int):
        try:
           return await RecentShema.query.where(RecentShema.user_id == id).gino.first()
        except Exception:
            return False
    
    async def get_shema(self):      
    #    custom_order = ['null', 'First reachout', 'Second reachout', 'Third reachout', 'Вернётся позже', 'Полный отказ']
    #    order_case = case(
    #    [(item, index) for index, item in enumerate(custom_order)],
    #    value=RecentShema.state,  # Замените column_name на реальное название столбца
    #    else_=''
    #)
    #    print(order_case)
        try:
           return await RecentShema.query.order_by(RecentShema.state.asc()).gino.all()
        except Exception as e:
            print(e)
            return False
    
    
    async def update_record(self, **kwargs):
        if not kwargs:
            
            return False
        try:
            recent = await self.select_recent()
            print('food')
            return await recent.update(**kwargs).apply()
        except Exception:
            return False


    async def remove(self):
        try:
            pay = await self.select_recent()
            print(1)
            return await pay.delete()
        except Exception:
            return False

class FirstRecent:
    def __init__(self, user_id: Optional[int] = None, state: Optional[str] = '0', username: Optional[str] = 'Не указано'):
        self.user_id = user_id
        self.state = state
        self.username = username
        
    async def add(self):
        try:
            first = FirstShema(user_id=self.user_id, state = self.state, username = self.username)    
            return await first.create()
        except UniqueViolationError:
            return False
    
    async def select_etap(self, etap: str):

        try:
         
            return await FirstShema.query.where(FirstShema.state == etap).gino.all()
        except Exception:
            return False
    
    async def select_recent(self):
    #    print(await FirstShema.query.where(FirstShema.user_id == self.user_id).gino.first())
        try:
         
            return await FirstShema.query.where(FirstShema.user_id == self.user_id).gino.first()
        except Exception:
            return False
        
    async def get_shema(self):
        try:
           return await FirstShema.query.order_by(FirstShema.state.asc()).gino.all()
        except Exception:
            return False
        
             
    async def check(self):
        try:
            if self.user_id:
                try:
                    d = await FirstShema.query.where(FirstShema.user_id == self.user_id).gino.all()
                    if len(d) != None:
                        return 2
                    else:
                        return 1

                except:
                    return 1
            else:
                return 1 
        except Exception:
            return 0     
       
    async def select_first(self):
        try:
            if self.user_id:
                return await FirstShema.query.where(FirstShema.user_id == self.user_id).gino.first()
        except Exception:
            return False
        
        
     
    async def update_record(self, **kwargs):
        if not kwargs:
            return False
        try:
            first = await self.select_first()
            print('food')
            return await first.update(**kwargs).apply()
        except Exception:
            return False


    async def remove(self):
        try:
            pay = await self.select_recent()
            return await pay.delete()
        except Exception:
            return False
    
class SecondRecent:
    def __init__(self, user_id: Optional[int] = None, state: Optional[str] = '0', username: Optional[str] = 'Не указано'):
        self.user_id = user_id
        self.state = state
        self.username = username
        
    async def add(self):
        try:
            second = SecondSchema(user_id=self.user_id, state = self.state, username = self.username)
            return await second.create()
        except UniqueViolationError:
            return False
    
    async def get_shema(self):
        try:
           return await SecondSchema.query.order_by(SecondSchema.state.asc()).gino.all()
        except Exception:
            return False
           
    
    
    async def select_recent(self):
        try:
     
            return await SecondSchema.query.where(SecondSchema.user_id == self.user_id).gino.first()
        except Exception:
            return False
    
    async def select_etap(self, etap: str):
        print(await SecondSchema.query.where(SecondSchema.state == etap).gino.all())
        try:
            return await SecondSchema.query.where(SecondSchema.state == etap).gino.all()
        except Exception:
            return False
    
       
    async def check(self):
        try:
            if self.user_id:
                try:
                    d = await SecondSchema.query.where(SecondSchema.user_id == self.user_id).gino.all()
                    if len(d) != None:
                        return 2
                    else:
                        return 1

                except:
                    return 1
            else:
                return 1 
        except Exception:
            return 0   
       
    async def select_second(self):
        try:
            if self.user_id:
                return await SecondSchema.query.where(SecondSchema.user_id == self.user_id).gino.first()
        except Exception:
            return False
        
        
     
    async def update_record(self, **kwargs):
        if not kwargs:
            return False
        try:
            second = await self.select_second()
            return await second.update(**kwargs).apply()
        except Exception:
            return False

    async def remove(self):
        try:
            pay = await self.select_recent()
            return await pay.delete()
        except Exception:
            return False

class ThirdRecent:
    def __init__(self, user_id: Optional[int] = None, state: Optional[str] = '0', username: Optional[str] = 'Не указано'):
        self.user_id = user_id
        self.state = state
        self.username = username
        
    async def add(self):
        try:
            third = ThirdSchema(user_id=self.user_id, state = self.state, username = self.username)
            return await third.create()
        except UniqueViolationError:
            return False
    
    async def select_recent(self):
        try:

            return await ThirdSchema.query.where(ThirdSchema.user_id == self.user_id).gino.first()
        except Exception:
            return False
        
    
    async def get_shema(self):
        try:
           return await ThirdSchema.query.order_by(ThirdSchema.state.asc()).gino.all()
        except Exception:
            return False
    
       
    async def select_etap(self, etap: str):
        print(await ThirdSchema.query.where(ThirdSchema.state == etap).gino.all())
        try:
            return await ThirdSchema.query.where(ThirdSchema.state == etap).gino.all()
        except Exception:
            return False
    
    
    
        
    async def check(self):
        try:
            if self.user_id:
                try:
                    d = await ThirdSchema.query.where(ThirdSchema.user_id == self.user_id).gino.all()
                    if len(d) != None:
                        return 2
                    else:
                        return 1

                except:
                    return 1
            else:
                return 1 
        except Exception:
            return 0   
       
    async def select_third(self):
        try:
            if self.user_id:
                return await ThirdSchema.query.where(ThirdSchema.user_id == self.user_id).gino.first()
        except Exception:
            return False
        
        
     
    async def update_record(self, **kwargs):
        if not kwargs:
            return False
        try:
            third = await self.select_third()
            return await third.update(**kwargs).apply()
        except Exception:
            return False

    async def remove(self):
        try:
            pay = await self.select_recent()
            return await pay.delete()
        except Exception:
            return False



class DbUser:
    def __init__(self, user_id: Optional[int] = None, role: Optional[str] = None, username: Optional[str] = None, name: Optional[str] = None, parent: Optional[int] = 0, referals_count: Optional[int] = 0):
        self.user_id = user_id
        self.role = role
        self.username = username
        self.name = name
        self.parent = parent
        self.referals_count = referals_count
    async def add(self):
        try:
            user = UserSchema(user_id=self.user_id, role=self.role, username=self.username, name=self.name, parent=self.parent)
            return await user.create()
        except UniqueViolationError:
            return False

    async def select_user(self):
        try:
            if self.user_id and not self.role:
                return await UserSchema.query.where(UserSchema.user_id == self.user_id).order_by(
                    UserSchema.id.desc()).gino.first()
            elif not self.user_id and self.role:
                return await UserSchema.query.where(UserSchema.role == self.role).gino.all()

            return await UserSchema.query.where(
                and_(UserSchema.user_id == self.user_id, UserSchema.role == self.role)).gino.first()
        except Exception:
            return False

    async def select_users_by_notification_and_role(self, notification: int, role: str):

        try:
            if (notification == -1):
                return await UserSchema.query.where(
                    and_(
                        UserSchema.notification != -1,
                        UserSchema.role == role,
                        UserSchema.bot_blocked.is_(False)
                    )
                ).gino.all()
            else:
                return await UserSchema.query.where(
                    and_(
                        UserSchema.notification == notification,
                        UserSchema.role == role,
                        UserSchema.bot_blocked.is_(False)
                    )
                ).gino.all()
        except Exception:
            return False

    async def get_users_by_role(self, role: str):
        try:
            return await UserSchema.query.where(UserSchema.role == role).gino.all()
        except Exception:
            return False

    async def set_state(self, state: str):
        try:
            user = await self.select_user()
            return await user.update(state=state).apply()
        except Exception:
            return False
    
    
    async def set_username(self, username: str):
        try:
            user = await self.select_user()
            return await user.update(username=username).apply()
        except Exception:
            return False
    
    
    async def get_state(self):
        try:
            user = await self.select_user()
            return user.state
        except Exception:
            return False

    async def get_referals_count(self):
        try:
            user = await self.select_user()
            return user.referals_count
        except Exception:
            return False

    async def remove(self):
        try:
            user = await self.select_user()
            return await user.delete()
        except Exception:
            return False

    async def update_record(self, **kwargs):
        if not kwargs:
            return False

        try:
            user = await self.select_user()
            print(user)
            return await user.update(**kwargs).apply()
        except Exception:
            print(Exception)
            return False

    async def update_bot_blocked(self, blocked: bool):
        await self.update_record(bot_blocked=blocked)

    async def update_username(self, username: str):
        await self.update_record(username=username)
        
    async def get_schema(self):
        try:
            return UserSchema
        except Exception:
            return False


class DbMessage:
    def __init__(self, key: Optional[str] = None, text: Optional[str] = None, lang: Optional[str] = None,
                 entity: Optional[str] = None):
        self.key = key
        self.text = text
        self.lang = lang
        self.entity = entity

    async def add(self):
        try:
            message = MessageSchema(key=self.key, text=self.text, lang=self.lang, entity=self.entity)
            return await message.create()
        except UniqueViolationError:
            return False

    async def select_message(self):
        try:
            if self.key:
                return await MessageSchema.query.where(MessageSchema.key == self.key).gino.first()
            if self.text:
                return await MessageSchema.query.where(MessageSchema.text == self.text).gino.first()
        except Exception:
            return False

    async def remove(self):
        try:
            message = await self.select_message()
            return await message.delete()
        except Exception:
            return False

    async def update_record(self, **kwargs):
        if not kwargs:
            return False

        try:
            message = await self.select_message()
            return await message.update(**kwargs).apply()
        except Exception:
            return False

    async def get_text(self):
        try:
            message = await self.select_message()
            return message.text
        except Exception:
            return False


class DbSetting:
    def __init__(self, key: Optional[str] = None, value: Optional[str] = None):
        self.key = key
        self.value = value

    async def add(self):
        try:
            setting = SettingSchema(key=self.key, value=self.value)
            return await setting.create()
        except UniqueViolationError:
            return False

    async def select_setting(self):
        try:
            if self.key:
                return await SettingSchema.query.where(SettingSchema.key == self.key).gino.first()
            if self.value:
                return await SettingSchema.query.where(SettingSchema.value == self.value).gino.first()
        except Exception:
            return False

    async def remove(self):
        try:
            setting = await self.select_setting()
            return await setting.delete()
        except Exception:
            return False

    async def update_record(self, **kwargs):
        if not kwargs:
            return False

        try:
            setting = await self.select_setting()
            return await setting.update(**kwargs).apply()
        except Exception:
            return False


class DbPay:
    def __init__(self, user_id: Optional[int] = None, amount: Optional[float] = None, plan: Optional[str] = None,
                 status: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None,
                 remaining: Optional[float] = None, id: Optional[int] = None, username: Optional[str] = None, name: Optional[str] = None):
        self.user_id = user_id
        self.amount = amount
        self.plan = plan
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.remaining = remaining
        self.id = id
        self.username = username
        self.name = name

    async def add(self):
        try:
            pay = PaySchema(user_id=self.user_id, amount=self.amount, plan=self.plan, status=self.status,
                            start_date=self.start_date, end_date=self.end_date, username=self.username, name=self.name)
            return await pay.create()
        except UniqueViolationError:
            return False

    async def select_pay(self):
        try:
            if self.id:
                return await PaySchema.query.where(PaySchema.id == self.id).gino.first()
            if self.user_id and self.plan and self.status and self.amount:
                return await PaySchema.query.where(and_(PaySchema.user_id == self.user_id, PaySchema.plan == self.plan,
                                                        PaySchema.status == self.status,
                                                        PaySchema.amount == self.amount)).gino.first()
            if self.user_id and self.plan and self.status:
                return await PaySchema.query.where(and_(PaySchema.user_id == self.user_id, PaySchema.plan == self.plan,
                                                        PaySchema.status == self.status)).gino.first()
            if self.user_id and self.status:
                return await PaySchema.query.where(
                    and_(PaySchema.user_id == self.user_id, PaySchema.status == self.status)).order_by(
                    PaySchema.id.desc()).gino.first()
            if self.user_id:
                return await PaySchema.query.where(PaySchema.user_id == self.user_id).order_by(
                    PaySchema.id.desc()).gino.first()
            if self.plan:
                return await PaySchema.query.where(PaySchema.plan == self.plan).gino.first()
        except Exception:
            return False

    async def remove(self):
        try:
            pay = await self.select_pay()
            return await pay.delete()
        except Exception:
            return False

    async def update_record(self, **kwargs):
        if not kwargs:
            return False

        try:
            pay = await self.select_pay()
            return await pay.update(**kwargs).apply()
        except Exception:
            return False

    async def get_pays_by_status(self, status: str):
        try:
            return await PaySchema.query.where(PaySchema.status == status).gino.all()
        except Exception:
            print(traceback.format_exc())
            return False

    async def get_pay_by_user_id(self, user_id: int):
        try:
            return await PaySchema.query.where(PaySchema.user_id == user_id).gino.first()
        except Exception:
            return False

    async def get_pay_by_status_and_user_id(self, status: str, user_id: int):
        try:
            return await PaySchema.query.where(
                and_(PaySchema.status == status, PaySchema.user_id == user_id)).gino.all()
        except Exception:
            return False

    async def get_pay_by_plan_and_status(self, plan: str, status: str):
        try:
            return await PaySchema.query.where(
                and_(PaySchema.plan == plan, PaySchema.status == status)).gino.all()
        except Exception:
            return False
    
    
    async def get_pays_before_date(self, date: str):
        try:
            return await PaySchema.query.where(PaySchema.end_date < date).order_by(PaySchema.plan).gino.all()
        except Exception:
            return False
    
    async def get_pays_after_date_and_status(self, date: str, status: str):
        try:
            return await PaySchema.query.where(
                and_(PaySchema.end_date > date, PaySchema.status == status)).order_by(PaySchema.plan).gino.all()
        except Exception:
            return False
        
        
    async def get_pays_before_date_and_plan(self, date: str, plan: str, st: str):
        try:
            return await PaySchema.query.where(
                and_(PaySchema.end_date < date, PaySchema.plan == plan, PaySchema.start_date > st)).gino.all()
        except Exception:
            return False

    
    async def get_pays_after_date(self, date: str):
        try:
            return await PaySchema.query.where(PaySchema.end_date > date).order_by(PaySchema.plan).gino.all()
        except Exception:
            return False

class DbTeam:
    def __init__(self, team_id: Optional[int] = None):
        self.team_id = team_id

    async def add_team(self, **kwargs):
        try:
            team = TeamSchema(**kwargs)
            return await team.create()
        except Exception:
            return False

    async def select_team(self):
        try:
            return await TeamSchema.query.where(TeamSchema.id == self.team_id).gino.first()
        except Exception:
            return False

    async def update_team(self, **kwargs):
        try:
            team = await self.select_team()
            return await team.update(**kwargs).apply()
        except Exception:
            return False
