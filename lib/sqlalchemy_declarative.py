import sys
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Float, create_engine
from sqlalchemy.dialects.mysql import DOUBLE, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')

Base = declarative_base()

db = "mysql+pymysql://{}:{}@{}/{}?host={}?port={}".format(config.get("database", 'user'),
                                                          config.get("database", 'password'),
                                                          config.get("database", 'host'),
                                                          config.get("database", 'db_name'),
                                                          config.get("database", 'host'),
                                                          config.get("database", 'port')
                                                          )



def db_connect(db=db, timeout=300):
    try:
        # Engine needs to be set to exact location for automation to work
        engine = create_engine(db, connect_args={'connect_timeout': timeout})
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        session = Session()
        Session.remove()
        return session, engine
    except Exception as e:
        print('Error setting up DB: ', str(e))
        print('Quitting')
        sys.exit()


def db_insert(df, tableName):
    session, engine = db_connect()
    # Insert into DB
    df.to_sql(tableName, engine, if_exists='append', index=True)
    engine.dispose()
    session.close()


##### Athlete Table #####

class athlete(Base):
    __tablename__ = 'athlete'
    athlete_id = Column('athlete_id', Integer(), index=True, primary_key=True, autoincrement=True)
    name = Column('name', String(255))
    birthday = Column('birthday', Date())
    sex = Column('sex', String(1))
    min_non_warmup_workout_time = Column('min_non_warmup_workout_time', Integer())
    weekly_tss_goal = Column('weekly_tss_goal', Integer())
    rr_max_goal = Column('rr_max_goal', Integer())
    rr_min_goal = Column('rr_min_goal', Integer())
    weekly_workout_goal = Column('weekly_workout_goal', Integer())
    weekly_yoga_goal = Column('weekly_yoga_goal', Integer())
    weekly_sleep_score_goal = Column('weekly_sleep_score_goal', Integer())
    weekly_readiness_score_goal = Column('weekly_readiness_score_goal', Integer())
    weekly_activity_score_goal = Column('weekly_activity_score_goal', Integer())
    daily_sleep_hr_target = Column('daily_sleep_hr_target', Integer())
    ftp_test_notification_week_threshold = Column('ftp_test_notification_week_threshold', Integer())
    cycle_power_zone_threshold_1 = Column('cycle_power_zone_threshold_1', DOUBLE())
    cycle_power_zone_threshold_2 = Column('cycle_power_zone_threshold_2', DOUBLE())
    cycle_power_zone_threshold_3 = Column('cycle_power_zone_threshold_3', DOUBLE())
    cycle_power_zone_threshold_4 = Column('cycle_power_zone_threshold_4', DOUBLE())
    cycle_power_zone_threshold_5 = Column('cycle_power_zone_threshold_5', DOUBLE())
    cycle_power_zone_threshold_6 = Column('cycle_power_zone_threshold_6', DOUBLE())
    run_power_zone_threshold_1 = Column('run_power_zone_threshold_1', DOUBLE())
    run_power_zone_threshold_2 = Column('run_power_zone_threshold_2', DOUBLE())
    run_power_zone_threshold_3 = Column('run_power_zone_threshold_3', DOUBLE())
    run_power_zone_threshold_4 = Column('run_power_zone_threshold_4', DOUBLE())
    hr_zone_threshold_1 = Column('hr_zone_threshold_1', DOUBLE())
    hr_zone_threshold_2 = Column('hr_zone_threshold_2', DOUBLE())
    hr_zone_threshold_3 = Column('hr_zone_threshold_3', DOUBLE())
    hr_zone_threshold_4 = Column('hr_zone_threshold_4', DOUBLE())


class hrvWorkoutStepLog(Base):
    __tablename__ = 'hrv_workout_step_log'
    id = Column('id', Integer(), index=True, primary_key=True, autoincrement=True)
    athlete_id = Column('athlete_id', Integer())
    date = Column('date', Date())
    hrv_workout_step = Column('hrv_workout_step', Integer())
    hrv_workout_step_desc = Column('hrv_workout_step_desc', String(20))
    completed = Column('completed', Boolean, default=False)
    rationale = Column('rationale', String(255))


class annotations(Base):
    __tablename__ = 'annotations'
    id = Column('id', Integer(), index=True, primary_key=True, autoincrement=True)
    athlete_id = Column('athlete_id', Integer())
    date = Column('date', Date())
    annotation = Column('annotation', String(255))


##### Strava Tables #####

class stravaSamples(Base):
    __tablename__ = 'strava_samples'
    timestamp_local = Column('timestamp_local', DateTime(), index=True, primary_key=True)
    time_interval = Column('time_interval', DateTime())
    activity_id = Column('activity_id', BIGINT())
    date = Column('date', Date())
    type = Column('type', String(255))
    act_name = Column('act_name', String(255))
    athlete_id = Column('athlete_id', BIGINT())
    distance = Column('distance', DOUBLE())
    velocity_smooth = Column('velocity_smooth', DOUBLE())
    temp = Column('temp', DOUBLE())
    altitude = Column('altitude', DOUBLE())
    latitude = Column('latitude', DOUBLE())
    longitude = Column('longitude', DOUBLE())
    heartrate = Column('heartrate', Integer())
    cadence = Column('cadence', Integer())
    watts = Column('watts', Integer())
    moving = Column('moving', Integer())
    grade_smooth = Column('grade_smooth', DOUBLE())
    ftp = Column('ftp', DOUBLE())
    time = Column('time', Integer())
    power_zone = Column('power_zone', Integer())
    hr_zone = Column('hr_zone', Integer())
    hr_lowest = Column('hr_lowest', Integer())


class stravaBestSamples(Base):
    __tablename__ = 'strava_best_samples'
    activity_id = Column('activity_id', BIGINT(), index=True, primary_key=True)
    interval = Column('interval', Integer, index=True, primary_key=True)
    mmp = Column('mmp', DOUBLE())
    watts_per_kg = Column('watts_per_kg', DOUBLE())
    timestamp_local = Column('timestamp_local', DateTime())
    time_interval = Column('time_interval', DateTime())
    type = Column('type', String(255))
    date = Column('date', Date())
    act_name = Column('act_name', String(255))
    athlete_id = Column('athlete_id', BIGINT())


class stravaSummary(Base):
    __tablename__ = 'strava_summary'
    start_date_utc = Column('start_date_utc', DateTime(), index=True, primary_key=True)
    activity_id = Column('activity_id', BIGINT())
    athlete_id = Column('athlete_id', BIGINT())
    name = Column('name', String(255))
    distance = Column('distance', DOUBLE())
    moving_time = Column('moving_time', BIGINT())
    elapsed_time = Column('elapsed_time', BIGINT())
    total_elevation_gain = Column('total_elevation_gain', Integer())
    type = Column('type', String(255))
    start_date_local = Column('start_date_local', DateTime())
    start_day_local = Column('start_day_local', Date())
    timezone = Column('timezone', String(255))
    start_lat = Column('start_lat', String(255))
    start_lon = Column('start_lon', String(255))
    end_lat = Column('end_lat', String(255))
    end_lon = Column('end_lon', String(255))
    location_city = Column('location_city', String(255))
    location_state = Column('location_state', String(255))
    location_country = Column('location_country', String(255))
    average_speed = Column('average_speed', DOUBLE())
    max_speed = Column('max_speed', DOUBLE())
    average_watts = Column('average_watts', DOUBLE())
    max_watts = Column('max_watts', DOUBLE())
    average_heartrate = Column('average_heartrate', DOUBLE())
    max_heartrate = Column('max_heartrate', DOUBLE())
    kilojoules = Column('kilojoules', DOUBLE())
    device_name = Column('device_name', String(255))
    calories = Column('calories', DOUBLE())
    description = Column('description', String(255))
    pr_count = Column('pr_count', Integer())
    achievement_count = Column('achievement_count', Integer())
    commute = Column('commute', Integer())
    trainer = Column('trainer', Integer())
    gear_id = Column('gear_id', String(255))
    ftp = Column('ftp', DOUBLE())
    weighted_average_power = Column('weighted_average_power', DOUBLE())
    relative_intensity = Column('relative_intensity', DOUBLE())
    efficiency_factor = Column('efficiency_factor', DOUBLE())
    tss = Column('tss', DOUBLE())
    hrss = Column('hrss', DOUBLE())
    variability_index = Column('variability_index', DOUBLE())
    trimp = Column('trimp', DOUBLE())
    low_intensity_seconds = Column('low_intensity_seconds', Integer())
    med_intensity_seconds = Column('med_intensity_seconds', Integer())
    high_intensity_seconds = Column('high_intensity_seconds', Integer())
    weight = Column('weight', DOUBLE())


##### Oura Tables #####
class ouraReadinessSummary(Base):
    __tablename__ = 'oura_readiness_summary'
    report_date = Column('report_date', Date(), index=True, primary_key=True)
    summary_date = Column('summary_date', Date())
    score = Column('score', Integer())
    period_id = Column('period_id', Integer())
    score_activity_balance = Column('score_activity_balance', Integer())
    score_previous_day = Column('score_previous_day', Integer())
    score_previous_night = Column('score_previous_night', Integer())
    score_recovery_index = Column('score_recovery_index', Integer())
    score_resting_hr = Column('score_resting_hr', Integer())
    score_sleep_balance = Column('score_sleep_balance', Integer())
    score_temperature = Column('score_temperature', Integer())
    score_hrv_balance = Column('score_hrv_balance', Integer())


class ouraActivitySummary(Base):
    __tablename__ = 'oura_activity_summary'
    summary_date = Column('summary_date', Date(), index=True, primary_key=True)
    average_met = Column('average_met', DOUBLE())
    cal_active = Column('cal_active', Integer())
    cal_total = Column('cal_total', Integer())
    class_5min = Column('class_5min', String(300))
    daily_movement = Column('daily_movement', Integer())
    day_end_local = Column('day_end_local', DateTime())
    day_start_local = Column('day_start_local', DateTime())
    high = Column('high', Integer())
    inactive = Column('inactive', Integer())
    inactivity_alerts = Column('inactivity_alerts', Integer())
    low = Column('low', Integer())
    medium = Column('medium', Integer())
    met_min_high = Column('met_min_high', Integer())
    met_min_inactive = Column('met_min_inactive', Integer())
    met_min_low = Column('met_min_low', Integer())
    met_min_medium = Column('met_min_medium', Integer())
    non_wear = Column('non_wear', Integer())
    rest = Column('rest', Integer())
    score = Column('score', Integer())
    score_meet_daily_targets = Column('score_meet_daily_targets', Integer())
    score_move_every_hour = Column('score_move_every_hour', Integer())
    score_recovery_time = Column('score_recovery_time', Integer())
    score_stay_active = Column('score_stay_active', Integer())
    score_training_frequency = Column('score_training_frequency', Integer())
    score_training_volume = Column('score_training_volume', Integer())
    steps = Column('steps', Integer())
    target_calories = Column('target_calories', Integer())
    timezone = Column('timezone', Integer())
    target_km = Column('target_km', DOUBLE())
    target_miles = Column('target_miles', DOUBLE())
    to_target_km = Column('to_target_km', DOUBLE())
    to_target_miles = Column('to_target_miles', DOUBLE())
    total = Column('total', Integer())


class ouraActivitySamples(Base):
    __tablename__ = 'oura_activity_samples'
    timestamp_local = Column('timestamp_local', DateTime(), index=True, primary_key=True)
    summary_date = Column('summary_date', Date())
    met_1min = Column('met_1min', DOUBLE())
    class_5min = Column('class_5min', Integer())
    class_5min_desc = Column('class_5min_desc', String(10))


class ouraSleepSummary(Base):
    __tablename__ = 'oura_sleep_summary'
    report_date = Column('report_date', Date(), index=True, primary_key=True)
    summary_date = Column('summary_date', Date())
    awake = Column('awake', Integer())
    bedtime_end_local = Column('bedtime_end_local', DateTime())
    bedtime_end_delta = Column('bedtime_end_delta', Integer())
    bedtime_start_local = Column('bedtime_start_local', DateTime())
    bedtime_start_delta = Column('bedtime_start_delta', Integer())
    breath_average = Column('breath_average', DOUBLE())
    deep = Column('deep', Integer())
    duration = Column('duration', Integer())
    efficiency = Column('efficiency', Integer())
    hr_average = Column('hr_average', DOUBLE())
    hr_lowest = Column('hr_lowest', Integer())
    hypnogram_5min = Column('hypnogram_5min', String(255))
    is_longest = Column('is_longest', Integer())
    light = Column('light', Integer())
    midpoint_at_delta = Column('midpoint_at_delta', Integer())
    midpoint_time = Column('midpoint_time', Integer())
    onset_latency = Column('onset_latency', Integer())
    period_id = Column('period_id', Integer())
    rem = Column('rem', Integer())
    restless = Column('restless', Integer())
    rmssd = Column('rmssd', Integer())
    score = Column('score', Integer())
    score_alignment = Column('score_alignment', Integer())
    score_deep = Column('score_deep', Integer())
    score_disturbances = Column('score_disturbances', Integer())
    score_efficiency = Column('score_efficiency', Integer())
    score_latency = Column('score_latency', Integer())
    score_rem = Column('score_rem', Integer())
    score_total = Column('score_total', Integer())
    temperature_delta = Column('temperature_delta', DOUBLE())
    temperature_deviation = Column('temperature_deviation', DOUBLE())
    temperature_trend_deviation = Column('temperature_trend_deviation', DOUBLE())
    timezone = Column('timezone', Integer())
    total = Column('total', Integer())


class ouraSleepSamples(Base):
    __tablename__ = 'oura_sleep_samples'
    timestamp_local = Column('timestamp_local', DateTime(), index=True, primary_key=True)
    summary_date = Column('summary_date', Date())
    report_date = Column('report_date', Date())
    rmssd_5min = Column('rmssd_5min', Integer())
    hr_5min = Column('hr_5min', Integer())
    hypnogram_5min = Column('hypnogram_5min', Integer())
    hypnogram_5min_desc = Column('hypnogram_5min_desc', String(8))


class apiTokens(Base):
    __tablename__ = 'api_tokens'
    date_utc = Column('date_utc', DateTime(), index=True, primary_key=True)
    service = Column('service', String(255))
    tokens = Column('tokens', String(255))


class dbRefreshStatus(Base):
    __tablename__ = 'db_refresh'
    timestamp_utc = Column('timestamp_utc', DateTime(), index=True, primary_key=True)
    process = Column('process', String(255))
    truncate = Column('truncate', Boolean(), default=False)
    oura_status = Column('oura_status', String(255))
    strava_status = Column('strava_status', String(255))
    withings_status = Column('withings_status', String(255))
    fitbod_status = Column('fitbod_status', String(255))


class withings(Base):
    __tablename__ = 'withings'
    date_utc = Column('date_utc', DateTime(), index=True, primary_key=True)
    weight = Column('weight', DOUBLE())
    fat_ratio = Column('fat_ratio', DOUBLE())
    hydration = Column('hydration', DOUBLE())


class fitbod(Base):
    __tablename__ = 'fitbod'
    id = Column('id', Integer(), index=True, primary_key=True, autoincrement=True)
    date_utc = Column('date_UTC', DateTime())
    exercise = Column('Exercise', String(255))
    reps = Column('Reps', Integer())
    weight = Column('Weight', Integer())
    duration = Column('Duration', Integer())
    iswarmup = Column('isWarmup', Boolean())
    note = Column('Note', String(255))
    one_rep_max = Column('one_rep_max', DOUBLE())
    weight_duration_max = Column('weight_duration_max', DOUBLE())


class fitbod_muscles(Base):
    __tablename__ = 'fitbod_muscles'
    exercise = Column('Exercise', String(255), index=True, primary_key=True)
    muscle = Column('Muscle', String(255))


session, engine = db_connect()
Base.metadata.create_all(engine)
engine.dispose()
session.close()