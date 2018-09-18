

class Bootstrap:
    def __init__(self):
        return True

    def getHeaders(self):
        script =   '''
        <!-- Bootstrap core CSS -->
        <link href="https://getbootstrap.com/docs/4.1/dist/css/bootstrap.min.css" rel="stylesheet">

        <!-- Custom styles for this template -->
        <link href="https://getbootstrap.com/docs/4.1/examples/starter-template/starter-template.css" rel="stylesheet">
        '''

        return script


    def getScript(self):
        script='''
         <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="https://getbootstrap.com/docs/4.1/assets/js/vendor/jquery-slim.min.js"><\/script>')</script>
    <script src="https://getbootstrap.com/docs/4.1//assets/js/vendor/popper.min.js"></script>
    <script src="https://getbootstrap.com/docs/4.1//dist/js/bootstrap.min.js"></script>
        '''
        return script