import json
import logging
from datetime import datetime, date
from aiogram.dispatcher import FSMContext
from django.contrib.auth.hashers import check_password
from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, executor, types
from app_goals.models import Goal, UserImpact, Operation
from app_users.models import Profile
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton
from django.contrib.auth import authenticate, login


logging.basicConfig(level=logging.INFO)

API_TOKEN = "5504415324:AAHWdeCwWeDyJAtPYEvhgqNU3IDE1gAKMk4"
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    login = State()
    username = State()
    password = State()


class GoalState(StatesGroup):
    action = State()
    goal = State()
    refill = State()


user = None
goals = None
goal_titles = []


@dp.message_handler(commands=['start', 'logout'])
@dp.message_handler(text='Выйти')
async def send_welcome(message: types.Message):
    text = 'Бот - копилка. Копите на свои мечты, выполняйте поставленные цели.\n' \
           'Бот создан для удобной работы с сайтом PurposesKeeper <ссылка на сайт>\n\n' \
           '/start - перезапустить бота, выйти из профиля\n' \
           '/login - войти\n' \
           '/url - ссылка на сайт\n'

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    login_btn = KeyboardButton('Войти')
    keyboard.add(login_btn)

    await message.answer(text, reply_markup=keyboard)
    await UserState.login.set()


@dp.message_handler(commands=['help'])
async def get_help(message: types.Message):
    text = 'Бот - копилка. Копите на свои мечты, выполняйте поставленные цели.\n' \
           'Бот создан для удобной работы с сайтом PurposesKeeper <ссылка на сайт>\n\n' \
           '/start - перезапустить бота, выйти из профиля\n' \
           '/login - войти\n' \
           '/url - ссылка на сайт\n'

    await message.answer(text)


@dp.message_handler(commands=['login'], state=UserState.login)
@dp.message_handler(text='Войти', state=UserState.login)
async def get_username(message: types.Message):
    text = 'введите имя пользователя или email'
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
    await UserState.username.set()
    # elif state == 'auth_success':
    #     text = 'Вы уже вошли, нажмите /start чтобы выйти'
    #     await message.answer(text)


@sync_to_async
def check_auth(username, password):
    global state, user
    try:
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            return True
        else:
            user = None
            return False
    except:
        user = None
        return False


@dp.message_handler(state=UserState.username)
async def get_password(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Введите пароль')
    await UserState.password.set()


@dp.message_handler(state=UserState.password)
async def auth(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    if await check_auth(data['username'], data['password']):
        text = f'Добро пожаловать, {user.username}\n'
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Выбрать цель'))
        await message.answer(text, reply_markup=keyboard)
        await state.finish()
    else:
        text = 'вы ввели неверный логин или пароль, нажмите /login'
        await message.answer(text)
        await UserState.login.set()


@sync_to_async
def get_goals(user):
    global goals, goal_titles
    goals = Goal.objects.filter(participants__in=[user])
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for goal in goals:
        keyboard.add(KeyboardButton(goal.title))
        goal_titles.append(goal.title)
    return keyboard


@dp.message_handler(text='Выбрать цель')
@dp.message_handler(text='Вернуться к списку')
async def get_goal_list(message: types.Message):
    global goals, goal_titles, user
    text = 'Выберите цель из списка'
    await message.answer(text, reply_markup=await get_goals(user))
    await GoalState.goal.set()


@dp.message_handler(state=GoalState.goal)
async def goal_action(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text)
    text = 'Выберите действие'
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_refill = KeyboardButton('Пополнить')
    btn_info = KeyboardButton('Информация')
    back_btn = KeyboardButton('Вернуться к списку')
    keyboard.add(btn_refill, btn_info, back_btn)
    await message.answer(text, reply_markup=keyboard)
    await GoalState.action.set()


@sync_to_async()
def get_goal_details(title):
    global user, your_impact, sum_impacts, timeleft
    goal = Goal.objects.get(title=title, participants__in=[user])
    impacts = UserImpact.objects.filter(goal=goal)
    your_impact = UserImpact.objects.get(goal=goal, user=user).impact
    sum_impacts = sum(user.impact for user in impacts)
    timeleft = (goal.deadline - date.today()).days
    return [sum_impacts, your_impact, timeleft]


@dp.message_handler(state=GoalState.action)
async def goal_info(message: types.Message, state: FSMContext):
    await state.update_data(action=message.text)
    data = await state.get_data()
    if data['action'] == 'Пополнить':
        text = 'Выберите сумму для пополнения или введите число без пробелов'
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        nums = [100, 200, 500, 1000, 2000, 5000, 10000]
        for i in nums:
            keyboard.add(KeyboardButton(str(i)))
        keyboard.add(KeyboardButton('Вернуться назад'))
        await message.answer(text, reply_markup=keyboard)
        await GoalState.refill.set()
    elif data['action'] == 'Информация':
        goal_data = await get_goal_details(data['goal'])
        text = f'Всего накоплено: {goal_data[0]}\n' \
               f'Накоплено вами: {goal_data[1]}\n' \
               f'Дней до дедлайна: {goal_data[2]}'
        await message.answer(text)
        await GoalState.action.set()
    elif data['action'] == 'Вернуться к списку':
        global goals, goal_titles, user
        text = 'Выберите цель из списка'
        await message.answer(text, reply_markup=await get_goals(user))
        await GoalState.goal.set()


@sync_to_async()
def refill(goal_title, user_impact):
    global user
    goal = Goal.objects.get(title=goal_title, participants__in=[user])
    try:
        impact = UserImpact.objects.get(user=user, goal=goal)
        impact.impact += int(user_impact)
        impact.save()
        Operation.objects.create(
            user=user,
            goal=goal,
            impact=user_impact
        )
        return True
    except:
        return False

@dp.message_handler(state=GoalState.refill)
async def goal_refill(message: types.Message, state: FSMContext):
    await state.update_data(refill=message.text)
    data = await state.get_data()
    if data['refill'] == 'Вернуться назад':
        text = 'Выберите действие'
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        btn_refill = KeyboardButton('Пополнить')
        btn_info = KeyboardButton('Информация')
        back_btn = KeyboardButton('Вернуться к списку')
        keyboard.add(btn_refill, btn_info, back_btn)
        await message.answer(text, reply_markup=keyboard)
        await GoalState.action.set()
    else:
        if await refill(data['goal'], data['refill']):
            text = 'Цель успешно пополнена'
        else:
            text = 'Что-то пошло не так, попробуйте снова'
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        btn_refill = KeyboardButton('Пополнить')
        btn_info = KeyboardButton('Информация')
        back_btn = KeyboardButton('Вернуться к списку')
        keyboard.add(btn_refill, btn_info, back_btn)
        await message.answer(text, reply_markup=keyboard)
        await GoalState.action.set()


####################################################################


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        executor.start_polling(dp, skip_updates=True)
