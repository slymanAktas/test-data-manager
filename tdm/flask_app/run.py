import sys
import os
from pathlib import Path

sys.path.append(str(Path(os.getcwd()).parent.parent))

from tdm.flask_app.all_services import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)