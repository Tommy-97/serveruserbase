
import datetime

from sqlalchemy.orm import Session

from models import Break, Norm, Planning, SessionLocal


def get_norm(equipment, work_type):
    session = SessionLocal()
    try:
        norm = session.query(Norm).filter_by(
            equipment=equipment, work_type=work_type).first()
        if norm:
            return {
                'productivity_per_hour': norm.productivity_per_hour,
                'setup_time': norm.setup_time
            }
        else:
            raise ValueError(
                "No norm found for the given equipment and work type")
    finally:
        session.close()


def get_breaks():
    session = SessionLocal()
    try:
        breaks = session.query(Break).all()
        return [
            {'break_start': brk.break_start,
                'break_duration': brk.break_duration, 'shift_type': brk.shift_type}
            for brk in breaks
        ]
    finally:
        session.close()


def get_operations(equipment):
    session = SessionLocal()
    try:
        operations = session.query(Planning).filter_by(
            equipment=equipment).order_by(Planning.priority).all()
        return [
            {
                'id': op.id,
                'work_type': op.work_type,
                'start_time': op.start_time,

                'required_operations': op.priority
            }
            for op in operations
        ]
    finally:
        session.close()


def update_operation_time(operation_id, start_time, end_time):
    session = SessionLocal()
    try:
        operation = session.query(Planning).filter_by(id=operation_id).first()
        if operation:
            operation.start_time = start_time
            operation.end_time = end_time
            session.commit()
    finally:
        session.close()


def update_operation_priority(operation_id, new_priority):
    session = SessionLocal()
    try:
        operation = session.query(Planning).filter_by(id=operation_id).first()
        if operation:
            operation.priority = new_priority
            session.commit()
    finally:
        session.close()


def get_operation_by_id(operation_id):
    session = SessionLocal()
    try:
        operation = session.query(Planning).filter_by(id=operation_id).first()
        if operation:
            return {
                'id': operation.id,
                'equipment': operation.equipment,
                'work_type': operation.work_type,
                'start_time': operation.start_time,

                'required_operations': operation.priority
            }
        else:
            raise ValueError("No operation found with the given ID")
    finally:
        session.close()


def calculate_production_time(equipment, work_type, start_time, required_operations):
    norm = get_norm(equipment, work_type)
    productivity_per_hour = norm['productivity_per_hour']
    setup_time = norm['setup_time']

    production_hours = required_operations / productivity_per_hour
    production_time = datetime.timedelta(hours=production_hours + setup_time)

    production_time_with_breaks = add_breaks(start_time, production_time)

    return start_time + production_time_with_breaks


def add_breaks(start_time, production_time):
    breaks = get_breaks()
    end_time = start_time + production_time
    production_time_with_breaks = production_time

    for brk in breaks:
        break_start = datetime.datetime.combine(
            start_time.date(), brk['break_start'])
        break_end = break_start + \
            datetime.timedelta(minutes=brk['break_duration'])

        if start_time <= break_start < end_time:
            production_time_with_breaks += datetime.timedelta(
                minutes=brk['break_duration'])

    return production_time_with_breaks


def update_operation_dates(equipment, start_time):
    operations = get_operations(equipment)

    for operation in operations:
        end_time = calculate_production_time(
            equipment, operation['work_type'], start_time, operation['required_operations'])
        update_operation_time(operation['id'], start_time, end_time)
        start_time = end_time


def change_priority(operation_id, new_priority):
    update_operation_priority(operation_id, new_priority)
    operation = get_operation_by_id(operation_id)
    update_operation_dates(operation['equipment'], operation['start_time'])
