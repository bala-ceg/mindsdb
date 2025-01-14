from mindsdb.integrations.libs.const import HANDLER_TYPE
from mindsdb.utilities import log

logger = log.getLogger(__name__)

from .__about__ import __description__ as description
from .__about__ import __version__ as version

try:
    from .mindsdb_inference_handler import MindsDBInferenceHandler as Handler

    import_error = None
except Exception as e:
    Handler = None
    import_error = e

title = "MindsDB Inference"
name = "mindsdb_inference"
type = HANDLER_TYPE.ML
permanent = True
__all__ = ["Handler", "version", "name", "type", "title", "description", "import_error"]