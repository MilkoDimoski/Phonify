using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Phonify.Migrations
{
    /// <inheritdoc />
    public partial class InitialCreate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Phones",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    vendor = table.Column<string>(type: "varchar(100)", unicode: false, maxLength: 100, nullable: false),
                    brand = table.Column<string>(type: "varchar(50)", unicode: false, maxLength: 50, nullable: false),
                    model = table.Column<string>(type: "varchar(100)", unicode: false, maxLength: 100, nullable: false),
                    whole_name = table.Column<string>(type: "varchar(200)", unicode: false, maxLength: 200, nullable: false),
                    price = table.Column<decimal>(type: "decimal(10,2)", nullable: false),
                    link = table.Column<string>(type: "text", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: true, defaultValueSql: "(getutcdate())"),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true, defaultValueSql: "(getutcdate())")
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK__Phones__3213E83F3715A692", x => x.id);
                });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Phones");
        }
    }
}
