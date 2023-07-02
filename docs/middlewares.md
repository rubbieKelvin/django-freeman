# Middlewares

Freeman provides a set of middlewares to help ease development

## FreemanPickMiddleware

Middleware that modifies the response of views by picking specific fields from JSON content.

This middleware is designed to work with Django web framework. It expects responses with a "Content-Type" header of "application/json". If the request has a "pick" query parameter with a valid JSON array of field names, this middleware will pick those fields from the JSON content of the response and return a new response with only those fields.

### Settings

#### FREEMAN_PICK_PARAM_NAME

Customize the query parameter field name:
By default, the FreemanPickMiddleware uses the "fields" query parameter field to specify the fields to pick from the JSON content. However, you can customize this field name by modifying the `FREEMAN_PICK_PARAM_NAME` setting in your Django project's settings.py file. For example:

```python
FREEMAN_PICK_PARAM_NAME = "pick"
```

### Behavior

The `FreemanPickMiddleware` performs the following steps when processing a request:

1. The `__call__` method is invoked with the incoming `HttpRequest` object.

2. The middleware checks if the response has a "Content-Type" header of "application/json". If not, the original response is returned unchanged.

3. If the response has a "Content-Type" header of "application/json", the middleware attempts to parse the JSON content of the response.

4. The middleware then checks if the request has a "pick" query parameter. If present, the parameter is expected to be a valid JSON array of field names.

5. If the "pick" query parameter is present, the middleware attempts to parse it as a JSON array. If it fails to parse, a `json.decoder.JSONDecodeError` is raised.

6. The middleware uses the `pick` function from the

`freeman.utils.picking` module to select only the specified fields from the JSON content.

7. The modified JSON content is serialized back to a string and assigned to the `content` attribute of the response.

8. The modified response is returned.

### Exceptions

- `json.decoder.JSONDecodeError`: If the "pick" query parameter is present but not a valid JSON array, a `json.decoder.JSONDecodeError` is raised with an appropriate error message.

### Example

To use the `FreemanPickMiddleware`, you need to include it in the `MIDDLEWARE` setting in your Django project's settings.py file. For example:

```python
MIDDLEWARE = [
    ...
    "freeman.middlewares.picking.FreemanPickMiddleware",
    ...
]
```

Once the middleware is included, you can make requests to your Django views with a "pick" query parameter containing a valid JSON array of field names. The middleware will pick only those fields from the JSON content of the response and return a modified response with the selected fields.

## FreemanExceptionHandlerMiddleware

Middleware that handles exceptions raised during request processing and generates appropriate error responses.

This middleware is designed to work with Django web framework. It intercepts exceptions that occur during the processing of a request and generates a JSON error response with the details of the exception.

### Behavior

The `FreemanExceptionHandlerMiddleware` performs the following steps when processing a request:

1. The `__call__` method is invoked with the incoming `HttpRequest` object.

2. The middleware allows the request to proceed to the next middleware or view by returning the response from the `get_response` callable.

3. If an exception is raised during the processing of the request, the `process_exception` method is invoked with the request object and the exception.

4. If the exception is of type `RequestError` (imported from `freeman.utils.exceptions`), the middleware logs the exception and generates a JSON error response.

5. The JSON error response contains the exception details in the "error" field, and the status code and headers are set according to the exception properties.

6. The JSON error response is returned as the final response for the request.

### Example

To use the `FreemanExceptionHandlerMiddleware`, you need to include it in the `MIDDLEWARE` setting in your Django project's settings.py file. For example:

```python
MIDDLEWARE = [
    ...
    'freeman.middlewares.errorhandling.FreemanExceptionHandlerMiddleware',
    ...
]
```

Once the middleware is included, any exceptions of type `RequestError` that occur during request processing will be caught and converted to JSON error responses with appropriate status codes and headers.
