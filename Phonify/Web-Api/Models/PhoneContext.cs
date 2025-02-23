using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;


namespace Phonify.Models;

public partial class PhoneContext : DbContext
{
    public PhoneContext()
    {
    }

    public PhoneContext(DbContextOptions<PhoneContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Phone> Mobile { get; set; }

    

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Phone>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PK__Phones__3213E83F3715A692");

            entity.Property(e => e.Id).HasColumnName("id");
            entity.Property(e => e.Brand)
                .HasMaxLength(50)
                .IsUnicode(false)
                .HasColumnName("brand");
            entity.Property(e => e.CreatedAt)
                .HasDefaultValueSql("(getutcdate())")
                .HasColumnName("created_at");
            entity.Property(e => e.Link)
                .HasColumnType("text")
                .HasColumnName("link");
            entity.Property(e => e.Model)
                .HasMaxLength(100)
                .IsUnicode(false)
                .HasColumnName("model");
            entity.Property(e => e.Price)
                .HasColumnType("decimal(10, 2)")
                .HasColumnName("price");
            entity.Property(e => e.UpdatedAt)
                .HasDefaultValueSql("(getutcdate())")
                .HasColumnName("updated_at");
            entity.Property(e => e.Vendor)
                .HasMaxLength(100)
                .IsUnicode(false)
                .HasColumnName("vendor");
            entity.Property(e => e.WholeName)
                .HasMaxLength(200)
                .IsUnicode(false)
                .HasColumnName("whole_name");
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
