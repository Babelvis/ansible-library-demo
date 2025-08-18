using System.ComponentModel.DataAnnotations;
using System.Text.RegularExpressions;

namespace api_dotnet_src;

public static class InputChecker
{
    public static void CheckCharacter(string id)
    {
        if (!Regex.IsMatch(id, @"^[A-Z]$"))
        {
            throw new ValidationException($"Invalid character: {id}, must be a single upper character");
        }
    }
    
    public static void CheckNumber(int number)
    {
        if (number is < 1 or > 255)
        {
            throw new ValidationException($"Invalid number: {number}, must be between 1 and 255");
        }
    }
}