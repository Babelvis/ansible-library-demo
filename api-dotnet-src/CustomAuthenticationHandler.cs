using System.Security.Claims;
using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Options;
namespace api_dotnet_src;

public class CustomAuthenticationHandler : AuthenticationHandler<CustomAuthenticationSchemeOptions>
{
    public CustomAuthenticationHandler(IOptionsMonitor<CustomAuthenticationSchemeOptions> options, ILoggerFactory logger, UrlEncoder encoder, ISystemClock clock) : base(options, logger, encoder, clock)
    {
    }

    public CustomAuthenticationHandler(IOptionsMonitor<CustomAuthenticationSchemeOptions> options, ILoggerFactory logger, UrlEncoder encoder) : base(options, logger, encoder)
    {
    }

    protected override Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        
        if (!Request.Headers.ContainsKey(CustomAuthenticationSchemeOptions.AuthorizationHeaderName))
        {
            return Task.FromResult(AuthenticateResult.Fail("Unauthorized"));
        }
        var authenticationHeaderValue = Request.Headers[CustomAuthenticationSchemeOptions.AuthorizationHeaderName];
        if (string.IsNullOrEmpty(authenticationHeaderValue))
        {
            return Task.FromResult(AuthenticateResult.NoResult());
        }
        
        if (authenticationHeaderValue != "secret")
        {
            return Task.FromResult(AuthenticateResult.Fail("Unauthorized"));
        }
        
        var claimsIdentity = new ClaimsIdentity(new List<Claim>(), Scheme.Name);
        var claimsPrincipal = new ClaimsPrincipal(claimsIdentity);
        return Task.FromResult(AuthenticateResult.Success(new AuthenticationTicket(claimsPrincipal,Scheme.Name)));
    }
}