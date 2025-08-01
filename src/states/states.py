from aiogram.fsm.state import State, StatesGroup


class SearchVehicleStates(StatesGroup):
    waiting_for_vehicle_id = State()


class GeozoneStates(StatesGroup):
    selected = State()

