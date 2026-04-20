class LoggingMixin:
    def log(self, message):
        print(f"[LOG] {message}")

class TimestampMixin:
    def created_at(self):
        from datetime import datetime
        return datetime.now()
    
class Process(LoggingMixin, TimestampMixin):
    def run(self):
        self.log(f"Proceso iniciado el {self.created_at()}")
        
def main():
    process = Process()
    process.run()

if __name__ == "__main__":
    main()