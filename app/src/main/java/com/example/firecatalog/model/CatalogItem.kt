package com.example.firecatalog.model

import java.io.Serializable

/**
 * One item in the catalog (e.g. a product, movie, or photo).
 * Implements Serializable so it can be passed between activities via an Intent extra.
 */
data class CatalogItem(
    val id: Long,
    val title: String,
    val description: String,
    val category: String,
    val imageUrl: String
) : Serializable

/**
 * Sample in-memory catalog data. Replace this with a real network/database
 * call (e.g. Retrofit) when you're ready to hook up a live source.
 */
object SampleCatalog {

    fun load(): List<CatalogItem> = listOf(
        CatalogItem(
            id = 1,
            title = "Trail Runner Jacket",
            description = "A lightweight, water-resistant jacket built for long trail runs " +
                "in unpredictable weather. Packs down into its own pocket.",
            category = "Outdoor Gear",
            imageUrl = "https://picsum.photos/id/1015/600/340"
        ),
        CatalogItem(
            id = 2,
            title = "Ceramic Pour-Over Set",
            description = "A hand-glazed ceramic dripper and carafe for slow, " +
                "flavorful coffee brewing at home.",
            category = "Kitchen",
            imageUrl = "https://picsum.photos/id/431/600/340"
        ),
        CatalogItem(
            id = 3,
            title = "Desk Lamp, Walnut Base",
            description = "A warm-toned LED desk lamp with a solid walnut base " +
                "and three brightness settings.",
            category = "Home",
            imageUrl = "https://picsum.photos/id/201/600/340"
        ),
        CatalogItem(
            id = 4,
            title = "Canvas Backpack",
            description = "A durable waxed-canvas backpack with a padded laptop " +
                "sleeve and leather trim.",
            category = "Outdoor Gear",
            imageUrl = "https://picsum.photos/id/103/600/340"
        ),
        CatalogItem(
            id = 5,
            title = "Cast Iron Skillet",
            description = "A pre-seasoned 10-inch cast iron skillet, oven safe " +
                "and built to last for generations.",
            category = "Kitchen",
            imageUrl = "https://picsum.photos/id/292/600/340"
        ),
        CatalogItem(
            id = 6,
            title = "Wool Throw Blanket",
            description = "A soft, oversized throw woven from merino wool. " +
                "Machine washable and available in five colors.",
            category = "Home",
            imageUrl = "https://picsum.photos/id/1060/600/340"
        ),
        CatalogItem(
            id = 7,
            title = "Insulated Water Bottle",
            description = "Keeps drinks cold for 24 hours or hot for 12. " +
                "Made from recycled stainless steel.",
            category = "Outdoor Gear",
            imageUrl = "https://picsum.photos/id/1025/600/340"
        ),
        CatalogItem(
            id = 8,
            title = "Chef's Knife",
            description = "An 8-inch forged chef's knife with a full tang " +
                "and a comfortable walnut handle.",
            category = "Kitchen",
            imageUrl = "https://picsum.photos/id/312/600/340"
        )
    )
}
