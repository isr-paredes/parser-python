class FileOpener:
    def __enter__(self):
        self.file = open('file.txt')
        return self.file
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
