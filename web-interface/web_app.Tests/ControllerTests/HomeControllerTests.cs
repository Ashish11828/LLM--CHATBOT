using System.Net;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Moq;
using web_interface.Controllers;
using web_interface.Models;
using web_interface.Services.Interfaces;

namespace web_interface.Tests.Controllers;

public class HomeControllerTests
{
    private readonly HomeController _sut; // Service Under Test
    private readonly Mock<ILogger<HomeController>> _loggerMock = new();
    private readonly Mock<IHttpService> _httpServiceMock = new();
    private readonly Mock<HttpContext> _httpContextMock = new();
    private readonly Mock<HttpResponse> _httpResponseMock = new();

    public HomeControllerTests()
    {
        _sut = new HomeController(_loggerMock.Object, _httpServiceMock.Object)
        {
            ControllerContext = new ControllerContext()
            {
                HttpContext = _httpContextMock.Object
            }
        };
    }

    [Fact]
    public async Task Prompt_ShouldReturnValidViewAndModel_WhenValidPrompt()
    {
        // Arrange
        var responseContentString = "{\"perplexica_response\":\"Six legs\"}";
        var testApiResponse = new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = new StringContent(responseContentString)
        };

        var testPrompt = "How many legs do ants have?";
        var path = $"api/handle-prompt?p={testPrompt}";

        _httpServiceMock.Setup(x => x.GetAsync(path))
            .ReturnsAsync(testApiResponse);

        PromptModel initPromptData = new()
        {
            Prompt = testPrompt
        };

        // Act
        var result = await _sut.Prompt(initPromptData);

        // Assert
        var viewResult = Assert.IsType<ViewResult>(result);
        var model = Assert.IsAssignableFrom<PromptModel>(viewResult.Model);
        Assert.Equal(responseContentString, model.Response);
    }

    [Fact]
    public async Task Prompt_ShouldReturnNonOkStatus_WhenInvalidPrompt()
    {
        // Arrange
        var responseContentString = "{\"error\":\"error message\"}";
        var testApiResponse = new HttpResponseMessage(HttpStatusCode.BadRequest)
        {
            Content = new StringContent(responseContentString)
        };

        var testPrompt = "ab";
        var path = $"api/handle-prompt?p={testPrompt}";

        _httpResponseMock.SetupProperty(r => r.StatusCode);
        _httpContextMock.SetupGet(c => c.Response).Returns(_httpResponseMock.Object);

        _httpServiceMock.Setup(x => x.GetAsync(path))
            .ReturnsAsync(testApiResponse);

        PromptModel initPromptData = new()
        {
            Prompt = testPrompt
        };

        // Act
        var result = await _sut.Prompt(initPromptData);

        // Assert
        var viewResult = Assert.IsType<ViewResult>(result);
        Assert.Equal((int)HttpStatusCode.BadRequest, _httpResponseMock.Object.StatusCode);
        var model = Assert.IsAssignableFrom<PromptModel>(viewResult.Model);
        Assert.Contains("error", model.Response);
    }
}
