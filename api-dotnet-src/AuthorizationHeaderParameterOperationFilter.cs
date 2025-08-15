using System.Reflection;
using Microsoft.AspNetCore.Authorization;
using Microsoft.OpenApi.Any;
using Microsoft.OpenApi.Models;
using Swashbuckle.AspNetCore.SwaggerGen;

namespace api_dotnet_src;

public class AuthorizationHeaderParameterOperationFilter : IOperationFilter
{
    public void Apply(OpenApiOperation operation, OperationFilterContext context)
    {
        context.ApiDescription.TryGetMethodInfo(out MethodInfo methodInfo);
        if (methodInfo == null || methodInfo.DeclaringType == null)
        {
            return;
        }

        var hasAllowAnonymousAttribute = false;

        if (methodInfo.MemberType == MemberTypes.Method)
        {
            // NOTE: Check the controller or the method itself has AllowAnonymousAttribute attribute
            hasAllowAnonymousAttribute =
                methodInfo.DeclaringType.GetCustomAttributes(true).OfType<AllowAnonymousAttribute>().Any() ||
                methodInfo.GetCustomAttributes(true).OfType<AllowAnonymousAttribute>().Any();
        }

        if (!hasAllowAnonymousAttribute)
        {
            if (operation.Parameters == null)
                operation.Parameters = new List<OpenApiParameter>();

            operation.Parameters.Add(new OpenApiParameter
            {
                Name = CustomAuthenticationSchemeOptions.AuthorizationHeaderName,
                In = ParameterLocation.Header,
                Description = "access token",
                Required = true,
                Schema = new OpenApiSchema
                {
                    Type = "string",
                    Default = new OpenApiString("secret")
                }
            });
        }
    }
}