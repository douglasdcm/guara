from guara import Application
from guara.abstract_transaction import AbstractTransaction

app = Application(driver="selenium")

app.add(AbstractTransaction())
app.run()
# it doesn't work, sadly