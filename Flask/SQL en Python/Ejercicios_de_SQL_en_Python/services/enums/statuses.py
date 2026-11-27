from enum import StrEnum

# Transiciones de estado para user

# active -> inactive
# active -> delinquent
# delinquent -> active
# inactive -> active 

class UserStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELINQUENT = "delinquent"

# Transiciones de estado para car

# available -> reserved -> rented -> available
# available -> maintenance -> available
# available o maintenance -> inactive o sold.
class CarStatus(StrEnum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    RENTED = "rented"
    MAINTENANCE = "maintenance"
    INACTIVE = "inactive"
    SOLD = "sold"

# Transiciones de estado para car_rental

# pending -> active -> completed
# active -> overdue -> completed
# pending -> cancelled
class CarRentalStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"



