# Fire Catalog App

A simple two-screen Fire TV (Android TV) app built with the Leanback library:

1. **Home / Catalog screen** — a browsable grid of items grouped into rows by
   category (`CatalogFragment`, using `BrowseSupportFragment`). Uses the
   D-pad to move focus between cards, matching standard Fire TV navigation.
2. **Details screen** — shown when an item is selected. Displays a larger
   image, title, description, and a "Back" button (`DetailsActivity`).

Sample data (8 items across 3 categories) lives in `SampleCatalog.kt` and
loads placeholder images from picsum.photos over the network. Swap that
object out for a real API/database call when you're ready.

## Opening the project

1. Install [Android Studio](https://developer.android.com/studio) (Hedgehog
   or newer recommended).
2. `File > Open` and select the `FireCatalogApp` folder.
3. Let Gradle sync — it will download the Android Gradle Plugin, Kotlin
   plugin, Leanback, and Glide automatically the first time.

## Running on a real Fire TV / Fire Stick

Fire TV devices aren't reachable through the normal "Run" button unless
you connect over ADB first:

1. On the Fire TV: **Settings > My Fire TV > Developer options** — turn on
   *ADB debugging* and *Apps from Unknown Sources*.
2. Find the device's IP address: **Settings > My Fire TV > About > Network**.
3. From a terminal (with `adb` on your PATH):
   ```
   adb connect <FIRE_TV_IP_ADDRESS>:5555
   ```
4. In Android Studio, the device should now appear in the device dropdown —
   select it and press Run. Or build an APK and sideload it manually:
   ```
   ./gradlew assembleDebug
   adb -s <FIRE_TV_IP_ADDRESS>:5555 install -r app/build/outputs/apk/debug/app-debug.apk
   ```

## Running on the Android TV emulator

If you don't have a physical device handy, create an Android TV emulator in
Android Studio's Device Manager (any Android TV system image) and run the
app on it the normal way — the leanback grid and D-pad navigation behave the
same as on a real Fire TV.

## Things to customize before shipping

- **App banner & icon** (`res/drawable/app_banner.xml`, `app_icon.xml`) are
  solid-color placeholders required so the manifest resolves. Replace them
  with real 320×180px (banner) and 96×96px+ (icon) PNG assets.
- **Catalog data** — replace `SampleCatalog.load()` with a real data source.
- **App name / label** — `res/values/strings.xml` → `app_name`.
- **Package name** — currently `com.example.firecatalog`; rename via
  Android Studio's refactor tool before publishing to the Amazon Appstore.
