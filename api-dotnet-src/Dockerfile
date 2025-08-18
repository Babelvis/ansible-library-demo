FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

COPY *.csproj ./
# Restore as distinct layers
RUN dotnet restore

# Copy everything
COPY . ./
# Build and publish a release
RUN dotnet publish -o out

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:8.0
ENV ASPNETCORE_ENVIRONMENT=Development
WORKDIR /app
COPY --from=build /app/out .
ENTRYPOINT ["dotnet", "api-dotnet-src.dll"]