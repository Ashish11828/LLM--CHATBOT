using System.Net.Http;
using System.Threading.Tasks;

namespace web_interface.Services.Interfaces;

public interface IHttpService
{
    Task<HttpResponseMessage> GetAsync(string? requestUri);
}
