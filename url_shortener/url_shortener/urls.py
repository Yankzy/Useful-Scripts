
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from automate.schema import schema
from shortener.views import root


urlpatterns = [
    # admin urls
    path('admin/', admin.site.urls),

    # GraphQL API
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('<str:url_hash>/', root, name='root'),
    
]
