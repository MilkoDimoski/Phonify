using System;
using System.Collections.Generic;

namespace Phonify.Models;

public partial class Phone
{
    public int Id { get; set; }

    public string Vendor { get; set; } = null!;

    public string Brand { get; set; } = null!;

    public string Model { get; set; } = null!;

    public string WholeName { get; set; } = null!;

    public decimal Price { get; set; }

    public string Link { get; set; } = null!;

    public DateTime? CreatedAt { get; set; }

    public DateTime? UpdatedAt { get; set; }
}
