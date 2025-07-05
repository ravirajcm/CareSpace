import spaces_data
import doctors_data
import bookings_data
import calendars_data

class SpacesAPI:
    def __init__(self):
        self.df = spaces_data.load_spaces()

    def get_all(self):
        return self.df.copy()

    def get_by_id(self, space_id):
        return self.df[self.df['Space ID'] == str(space_id)]

    def filter(self, **kwargs):
        df = self.df
        for k, v in kwargs.items():
            df = df[df[k] == v]
        return df

    def add(self, data):
        self.df = self.df.append(data, ignore_index=True)
        spaces_data.save_spaces(self.df)

    def update(self, space_id, updates):
        idx = self.df[self.df['Space ID'] == str(space_id)].index
        for k, v in updates.items():
            self.df.loc[idx, k] = v
        spaces_data.save_spaces(self.df)

class DoctorsAPI:
    def __init__(self):
        self.df = doctors_data.load_doctors()

    def get_all(self):
        return self.df.copy()

    def get_by_id(self, doctor_id):
        return self.df[self.df['DoctorID'] == str(doctor_id)]

    def filter(self, **kwargs):
        df = self.df
        for k, v in kwargs.items():
            df = df[df[k] == v]
        return df

    def add(self, data):
        self.df = self.df.append(data, ignore_index=True)
        doctors_data.save_doctors(self.df)

    def update(self, doctor_id, updates):
        idx = self.df[self.df['DoctorID'] == str(doctor_id)].index
        for k, v in updates.items():
            self.df.loc[idx, k] = v
        doctors_data.save_doctors(self.df)

class BookingsAPI:
    def __init__(self):
        self.df = bookings_data.load_bookings()

    def get_all(self):
        return self.df.copy()

    def get_by_space_id(self, space_id):
        return self.df[self.df['Space ID'] == str(space_id)]

    def filter(self, **kwargs):
        df = self.df
        for k, v in kwargs.items():
            df = df[df[k] == v]
        return df

    def add(self, data):
        self.df = self.df.append(data, ignore_index=True)
        bookings_data.save_bookings(self.df)

    def update(self, booking_id, updates):
        # Assume booking_id is a combination of Space ID + Start Timestamp
        idx = self.df[(self.df['Space ID'] == booking_id[0]) & (self.df['Start Timestamp'] == booking_id[1])].index
        for k, v in updates.items():
            self.df.loc[idx, k] = v
        bookings_data.save_bookings(self.df)

class CalendarsAPI:
    def __init__(self):
        self.df = calendars_data.load_calendars()

    def get_all(self):
        return self.df.copy()

    def get_by_doctor(self, doctor_id):
        return self.df[self.df['Doctor_Id'] == str(doctor_id)]

    def filter(self, **kwargs):
        df = self.df
        for k, v in kwargs.items():
            df = df[df[k] == v]
        return df

    def add(self, data):
        self.df = self.df.append(data, ignore_index=True)
        calendars_data.save_calendars(self.df)

    def update(self, row_idx, updates):
        for k, v in updates.items():
            self.df.loc[row_idx, k] = v
        calendars_data.save_calendars(self.df)
