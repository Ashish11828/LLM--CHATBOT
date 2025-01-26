using System.Net.Http;
using System.Threading.Tasks;
using web_interface.Services.Interfaces;

namespace web_interface.Services;

// This service basically exists only so that units that need HttpClient can be tested
public class CoreHttpService : IHttpService
{
    private readonly HttpClient _httpClient;

    public CoreHttpService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    Task<HttpResponseMessage> IHttpService.GetAsync(string? requestUri)
    {
        return _httpClient.GetAsync(requestUri);
    }
}
