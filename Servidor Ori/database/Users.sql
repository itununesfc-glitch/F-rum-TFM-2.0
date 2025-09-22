-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 12 Eki 2019, 14:43:04
-- Sunucu sürümü: 10.4.6-MariaDB
-- PHP Sürümü: 7.1.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `Users`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `account`
--

CREATE TABLE `account` (
  `IP` longtext NOT NULL,
  `Time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `banlog`
--

CREATE TABLE `banlog` (
  `Username` longtext NOT NULL,
  `BannedBy` longtext NOT NULL,
  `Time` longtext NOT NULL,
  `Reason` longtext NOT NULL,
  `Date` longtext NOT NULL,
  `Status` longtext NOT NULL,
  `IP` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `casierlog`
--

CREATE TABLE `casierlog` (
  `PlayerID` int(11) NOT NULL,
  `Name` text NOT NULL,
  `State` text NOT NULL,
  `Timestamp` text NOT NULL,
  `Bannedby` text NOT NULL,
  `Time` text NOT NULL,
  `Reason` text NOT NULL,
  `date` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `conversation`
--

CREATE TABLE `conversation` (
  `id` int(11) NOT NULL,
  `hash` text NOT NULL,
  `player` int(11) NOT NULL,
  `text` text NOT NULL,
  `date` text NOT NULL,
  `readed` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `conversations`
--

CREATE TABLE `conversations` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `player` int(11) NOT NULL,
  `started` int(11) NOT NULL,
  `date` int(11) NOT NULL,
  `hash` text NOT NULL,
  `trash` int(11) NOT NULL DEFAULT 0,
  `etkilesim` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `favorites`
--

CREATE TABLE `favorites` (
  `id` int(11) NOT NULL,
  `player` int(11) NOT NULL,
  `data` int(11) NOT NULL,
  `mode` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `forums`
--

CREATE TABLE `forums` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `icon` text NOT NULL,
  `priv` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `iletisim`
--

CREATE TABLE `iletisim` (
  `id` int(11) NOT NULL,
  `kadi` text NOT NULL,
  `email` text NOT NULL,
  `kategori` text NOT NULL,
  `konu` text NOT NULL,
  `mesaj` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo için tablo yapısı `likes`
--

CREATE TABLE `likes` (
  `id` int(11) NOT NULL,
  `player` int(11) NOT NULL,
  `data` int(11) NOT NULL,
  `topic` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `loginlog`
--

CREATE TABLE `loginlog` (
  `username` longtext DEFAULT NULL,
  `ip` longtext NOT NULL,
  `yazi` longtext NOT NULL,
  `Timestamp` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `oyunlist`
--

CREATE TABLE `oyunlist` (
  `id` int(11) NOT NULL,
  `img` text NOT NULL,
  `text` text NOT NULL,
  `link` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `profilestribe`
--

CREATE TABLE `profilestribe` (
  `id` int(11) NOT NULL,
  `tribe` int(11) NOT NULL,
  `avatar` text NOT NULL,
  `lang` text NOT NULL,
  `aciklama` text NOT NULL,
  `reisg` int(11) NOT NULL DEFAULT 1,
  `msgg` int(11) NOT NULL DEFAULT 1,
  `msgaciklama` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `profilesuser`
--

CREATE TABLE `profilesuser` (
  `id` int(11) NOT NULL,
  `player` int(11) NOT NULL,
  `aciklama` text NOT NULL,
  `stonline` int(11) NOT NULL DEFAULT 1,
  `online` text NOT NULL,
  `hash` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `reports`
--

CREATE TABLE `reports` (
  `id` int(11) NOT NULL,
  `byid` int(11) NOT NULL,
  `reportid` int(11) NOT NULL,
  `reason` text NOT NULL,
  `mode` text NOT NULL,
  `link` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `section`
--

CREATE TABLE `section` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `icon` text NOT NULL,
  `forum` int(11) NOT NULL,
  `lang` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `topic`
--

CREATE TABLE `topic` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `section` int(11) NOT NULL,
  `player` int(11) NOT NULL,
  `date` text NOT NULL,
  `pinned` int(11) NOT NULL DEFAULT 0,
  `locked` int(11) NOT NULL DEFAULT 0,
  `etkilesim` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `topicm`
--

CREATE TABLE `topicm` (
  `id` int(11) NOT NULL,
  `player` int(11) NOT NULL,
  `topic` int(11) NOT NULL,
  `text` text NOT NULL,
  `handled` int(11) NOT NULL DEFAULT 0,
  `hreason` text NOT NULL,
  `hwho` int(11) NOT NULL,
  `date` text NOT NULL,
  `lastedit` text NOT NULL,
  `devtracker` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `chats`
--

CREATE TABLE `chats` (
  `ID` longtext NOT NULL,
  `Name` longtext NOT NULL,
  `Members` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `ippermaban`
--

CREATE TABLE `ippermaban` (
  `IP` longtext NOT NULL,
  `BannedBy` longtext NOT NULL,
  `Reason` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `tribe`
--

CREATE TABLE `tribe` (
  `Code` int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `Name` longtext NOT NULL,
  `Message` longtext NOT NULL DEFAULT '',
  `House` int(11) NOT NULL DEFAULT 0,
  `Ranks` longtext NOT NULL DEFAULT '0|${trad#TG_0}|0;0|${trad#TG_1}|0;2|${trad#TG_2}|0;3|${trad#TG_3}|0;4|${trad#TG_4}|32;5|${trad#TG_5}|160;6|${trad#TG_6}|416;7|${trad#TG_7}|932;8|${trad#TG_8}|2044;9|${trad#TG_9}|2046',
  `Historique` longtext NOT NULL DEFAULT '',
  `Members` longtext NOT NULL,
  `CreateTime` int(11) NOT NULL,
  `alimlar` int(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `userpermaban`
--

CREATE TABLE `userpermaban` (
  `Username` longtext NOT NULL,
  `Reason` longtext NOT NULL,
  `BannedBy` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `Username` longtext NOT NULL,
  `Password` longtext NOT NULL,
  `PlayerID` int(11) NOT NULL AUTO_INCREMENT UNIQUE,
  `Email` longtext NOT NULL DEFAULT '',
  `PrivLevel` longtext NOT NULL DEFAULT '1',
  `TitleNumber` int(11) NOT NULL DEFAULT 0,
  `FirstCount` int(11) NOT NULL DEFAULT 0,
  `CheeseCount` int(11) NOT NULL DEFAULT 0,
  `ShamanCheeses` int(11) NOT NULL DEFAULT 0,
  `ShopCheeses` int(11) NOT NULL DEFAULT 0,
  `ShopFraises` int(11) NOT NULL DEFAULT 0,
  `ShamanSaves` int(11) NOT NULL DEFAULT 0,
  `HardModeSaves` int(11) NOT NULL DEFAULT 0,
  `DivineModeSaves` int(11) NOT NULL DEFAULT 0,
  `BootcampCount` int(11) NOT NULL DEFAULT 0,
  `ShamanType` int(11) NOT NULL DEFAULT 0,
  `ShopItems` longtext NOT NULL DEFAULT '',
  `ShamanItems` longtext NOT NULL DEFAULT '',
  `Clothes` longtext NOT NULL DEFAULT '',
  `Look` longtext NOT NULL DEFAULT '1;0,0,0,0,0,0,0,0,0',
  `ShamanLook` longtext NOT NULL DEFAULT '0,0,0,0,0,0,0,0,0,0',
  `MouseColor` longtext NOT NULL DEFAULT '78583a',
  `ShamanColor` longtext NOT NULL DEFAULT '95d9d6',
  `RegDate` int(11) NOT NULL,
  `Badges` longtext NOT NULL DEFAULT '',
  `CheeseTitleList` longtext NOT NULL DEFAULT '',
  `FirstTitleList` longtext NOT NULL DEFAULT '',
  `ShamanTitleList` longtext NOT NULL DEFAULT '',
  `ShopTitleList` longtext NOT NULL DEFAULT '',
  `BootcampTitleList` longtext NOT NULL DEFAULT '',
  `HardModeTitleList` longtext NOT NULL DEFAULT '',
  `DivineModeTitleList` longtext NOT NULL DEFAULT '',
  `SpecialTitleList` longtext NOT NULL DEFAULT '',
  `BanHours` int(11) NOT NULL DEFAULT 0,
  `ShamanLevel` int(11) NOT NULL DEFAULT 1,
  `ShamanExp` int(11) NOT NULL DEFAULT 0,
  `ShamanExpNext` int(11) NOT NULL DEFAULT 32,
  `Skills` longtext NOT NULL DEFAULT '',
  `LastOn` int(11) NOT NULL DEFAULT 0,
  `FriendsList` longtext NOT NULL DEFAULT '',
  `IgnoredsList` longtext NOT NULL DEFAULT '',
  `Gender` int(11) NOT NULL DEFAULT 0,
  `Marriage` longtext NOT NULL DEFAULT '',
  `Gifts` longtext NOT NULL DEFAULT '',
  `Messages` longtext NOT NULL DEFAULT '',
  `SurvivorStats` longtext NOT NULL DEFAULT '0,0,0,0',
  `RacingStats` longtext NOT NULL DEFAULT '0,0,0,0',
  `DefilanteStats` longtext NOT NULL DEFAULT '0,0,0',
  `Consumables` longtext NOT NULL DEFAULT '0:10',
  `EquipedConsumables` longtext NOT NULL DEFAULT '0',
  `Pet` int(11) NOT NULL DEFAULT 0,
  `PetEnd` int(11) NOT NULL DEFAULT 0,
  `ShamanBadges` longtext NOT NULL DEFAULT '',
  `EquipedShamanBadge` int(11) NOT NULL DEFAULT 0,
  `TotemItemCount` int(11) NOT NULL DEFAULT 0,
  `Totem` longtext NOT NULL DEFAULT '',
  `CustomItems` longtext NOT NULL DEFAULT '',
  `TribeCode` int(11) NOT NULL DEFAULT 0,
  `TribeRank` int(11) NOT NULL DEFAULT 0,
  `TribeJoined` int(11) NOT NULL DEFAULT 0,
  `Tag` longtext NOT NULL DEFAULT '',
  `Time` int(11) NOT NULL DEFAULT 0,
  `Fur` int(11) NOT NULL DEFAULT 0,
  `FurEnd` int(11) NOT NULL DEFAULT 0,
  `Hazelnut` int(11) NOT NULL DEFAULT 0,
  `VipTime` int(11) NOT NULL DEFAULT 0,
  `OldNames` longtext NOT NULL DEFAULT '',
  `Avatar` text NOT NULL DEFAULT 'default.png',
  `Langue` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `missions`
--

CREATE TABLE `missions` (
  `userid` longtext NOT NULL,
  `missions` longtext NOT NULL,
  `time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `usertempban`
--

CREATE TABLE `usertempban` (
  `Username` longtext NOT NULL,
  `Reason` longtext NOT NULL,
  `Time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `usertempmute`
--

CREATE TABLE `usertempmute` (
  `Username` longtext NOT NULL,
  `Time` int(11) NOT NULL,
  `Reason` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
COMMIT;

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `conversation`
--
ALTER TABLE `conversation`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `conversations`
--
ALTER TABLE `conversations`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `forums`
--
ALTER TABLE `forums`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `iletisim`
--
ALTER TABLE `iletisim`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `oyunlist`
--
ALTER TABLE `oyunlist`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `profilestribe`
--
ALTER TABLE `profilestribe`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `profilesuser`
--
ALTER TABLE `profilesuser`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `section`
--
ALTER TABLE `section`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `topic`
--
ALTER TABLE `topic`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `topicm`
--
ALTER TABLE `topicm`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `conversation`
--
ALTER TABLE `conversation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Tablo için AUTO_INCREMENT değeri `conversations`
--
ALTER TABLE `conversations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Tablo için AUTO_INCREMENT değeri `favorites`
--
ALTER TABLE `favorites`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Tablo için AUTO_INCREMENT değeri `forums`
--
ALTER TABLE `forums`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `iletisim`
--
ALTER TABLE `iletisim`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Tablo için AUTO_INCREMENT değeri `likes`
--
ALTER TABLE `likes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- Tablo için AUTO_INCREMENT değeri `oyunlist`
--
ALTER TABLE `oyunlist`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Tablo için AUTO_INCREMENT değeri `profilestribe`
--
ALTER TABLE `profilestribe`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `profilesuser`
--
ALTER TABLE `profilesuser`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Tablo için AUTO_INCREMENT değeri `reports`
--
ALTER TABLE `reports`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Tablo için AUTO_INCREMENT değeri `section`
--
ALTER TABLE `section`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Tablo için AUTO_INCREMENT değeri `topic`
--
ALTER TABLE `topic`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `topicm`
--
ALTER TABLE `topicm`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
