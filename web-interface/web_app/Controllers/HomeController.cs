using System.Diagnostics;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using web_interface.Models;
using web_interface.Services.Interfaces;

namespace web_interface.Controllers;

public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;
    private readonly IHttpService _httpService;

    public HomeController(ILogger<HomeController> logger, IHttpService httpService)
    {
        _logger = logger;
        _httpService = httpService;
    }

    public IActionResult Index()
    {
        return View();
    }

    public IActionResult Privacy()
    {
        return View();
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public IActionResult Error()
    {
        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Prompt([FromForm] PromptModel promptData)
    {
        // "using" will automatically call Dispose() on the HttpResponseMessage object once it is
        // not used anymore (out of scope). It implements IDisposable
        using HttpResponseMessage response = await _httpService.GetAsync($"api/handle-prompt?p={promptData.Prompt}");

        var jsonData = await response.Content.ReadAsStringAsync();
        promptData.Response = jsonData;

        if (!response.IsSuccessStatusCode)
        {
            Response.StatusCode = (int)response.StatusCode;
        }

        return View("Index", promptData);
    }
}
