<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - My Bottle Application</title>
    <link rel="stylesheet" type="text/css" href="/static/content/bootstrap.min.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/style_infection_spread.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/site.css" />
    <link rel="stylesheet" type="text/css" href="/static/content/style_cell_colonies.css" />
    <script src="/static/scripts/modernizr-2.6.2.js"></script>
</head>

<body>
    <div class="navbar navbar-custom navbar-fixed-top">
        <div class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li class="logo">
                    <a href="/home">
                        <img src="/static/images/icon.png" alt="Logo">
                    </a>
                </li>
                <li class="links">
                    <div class="button-container">
                        <a href="/wolf_island" class="nav-button">Death and reproduction</a>
                        <a href="/infection_spread" class="nav-button">The spread of infection</a>
                        <a href="/cells_colonies" class="nav-button">Colonies of living cells</a>
                        <a href="/about" class="nav-button">About authors</a>
                    </div>
                </li>
            </ul>
        </div>
    </div>

    <div class="container body-content">
        {{!base}}
        <hr />
        <footer>
            <p>&copy; {{ year }} - My Bottle Application</p>
        </footer>
    </div>

    <script src="/static/scripts/jquery-1.10.2.js"></script>
    <script src="/static/scripts/bootstrap.js"></script>
    <script src="/static/scripts/respond.js"></script>

</body>
</html>
