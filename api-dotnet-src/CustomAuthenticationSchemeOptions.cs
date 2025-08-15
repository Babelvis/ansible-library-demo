using Microsoft.AspNetCore.Authentication;

namespace api_dotnet_src;

public class CustomAuthenticationSchemeOptions : AuthenticationSchemeOptions
{
    public const string DefaultScheme = "CustomAuthenticationScheme";
    public const string AuthorizationHeaderName = "X-Auth-Token";
}