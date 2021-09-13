from dash import Dash




class FlaskDash(Dash):
    
    
    def interpolate_index(self, **kwargs):
        # Inspect the arguments by printing them
        print(kwargs)
        return '''
                {app_entry}
                {config}
                {scripts}
                {renderer}
            '''.format(
            app_entry=kwargs['app_entry'],
            config=kwargs['config'],
            scripts=kwargs['scripts'],
            renderer=kwargs['renderer'])