PROGRAM calcGraaddagen;

USES math, sysutils, unix;

VAR
  graaddagenNu: integer;
  graaddagenVorig: integer;
  verbruikNu: integer;
  verbruikVorig: integer;
  ratioGraaddagen: real;
  verwachtVerbruik: real;
  verschilVerbruik: real;
  verschilInPerc: real;

BEGIN
  //unix.fpSystem('clear');
  writeLn('[hint] Bereken graaddagen hier: https://www.mindergas.nl/degree_days_calculation');
  write('Graaddagen vorig jaar? ');
  readLn(input, graaddagenVorig);
  write('Verbruik vorig jaar (m3)? ');
  readLn(input, verbruikVorig);
  write('Graaddagen nu? ');
  readLn(input, graaddagenNu);
  write('Verbruik nu (m3)? ');
  readLn(input, verbruikNu);

  ratioGraaddagen := graaddagenNu / graaddagenVorig;
  verwachtVerbruik := verbruikVorig * ratioGraaddagen;
  verschilVerbruik := verbruikNu / verwachtVerbruik * 100;
  verschilInPerc := 0 - (100 - verschilVerbruik);

  writeLn;
  writeLn('Verwacht verbruik dit jaar is ', Format('%.2f',[verwachtVerbruik]), ' m3');
  writeLn('Werkelijk verbruik was ', verbruikNu, ' m3');
  writeLn('Dus in verhouding ', Format('%.2f',[verschilVerbruik]), '% (', Format('%.2f',[verschilInPerc]), '%)');
END.
