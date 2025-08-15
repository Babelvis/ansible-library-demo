using System.Collections.Concurrent;
using api_dotnet_src;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddAuthorization();
builder.Services.AddAuthentication
        (CustomAuthenticationSchemeOptions.DefaultScheme)
    .AddScheme<CustomAuthenticationSchemeOptions, CustomAuthenticationHandler>
    (CustomAuthenticationSchemeOptions.DefaultScheme, 
        _ => { });

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen(c => c.OperationFilter<AuthorizationHeaderParameterOperationFilter>());
builder.Services.AddHttpContextAccessor();

var app = builder.Build();

app.UseSwagger();
app.UseSwaggerUI();

var list = new ConcurrentDictionary<string, int>();

app.MapPost("/token", [AllowAnonymous][Authorize]([FromBody]UsernamePassword usernameAndPassword) =>
{
    if (usernameAndPassword is { Username: "user", Password: "password" })
    {
        return Task.FromResult("secret");
    }

    throw new UnauthorizedAccessException("Invalid username or password");
}).WithName("GetToken");

app.MapGet("/character", [Authorize]() =>
{
    return list.ToArray().Select(b => b.Key);
}).WithName("ListOfCharacters");

app.MapGet("/character/{id}", [Authorize](string id) =>
{
    if (list.TryGetValue(id, out var number))
        return Task.FromResult(number);
    throw new KeyNotFoundException($"Character with id {id} not found");
}).WithName("GetCharacter");

app.MapPost("/character/{id}", [Authorize](int number, string id) =>
{
    if (list.TryGetValue(id, out var currentNumber))
    {
        if (!list.TryUpdate(id, number, currentNumber))
        {
            throw new KeyNotFoundException($"Character {id} update failed");
        }
    }
    else
    {
        throw new KeyNotFoundException($"Character with id {id} not found");
    }

    return Task.CompletedTask;
}).WithName("PostCharacter");

app.MapPut("/character/{id}", [Authorize](int number, string id) =>
{
    if (!list.TryAdd(id, number))
    {
        throw new KeyNotFoundException($"Character with id {id} already exists");
    }
    return Task.CompletedTask;
}).WithName("PutCharacter");

app.MapDelete("/character/{id}", [Authorize](string id) =>
{
    if (!list.TryRemove(id, out _))
    {
        throw new KeyNotFoundException($"Character with id {id} not found");
    }

    return Task.CompletedTask;
}).WithName("DeleteCharacter");

app.UseAuthentication();
app.UseAuthorization();

app.Run();