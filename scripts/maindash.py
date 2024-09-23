import dash

external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css','https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css']


app = dash.Dash(__name__,suppress_callback_exceptions=True,external_stylesheets=external_stylesheets)

app.title = "MDiNE Explorer"
type_storage="session"