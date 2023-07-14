package.path = package.path
..";/data/pktgen-21.02.0/?.lua;/data/pktgen-21.02.0/test/?.lua;/data/pktgen-21.02.0/app/?.lua;/data/pktgen-21.02.0/../?.lua"

require "Pktgen";

-- define the ports in use
local sendport = "0";

-- parameters to use
local burst = 1;
local rate = 0.1;

function main()
    -- get dstmac and count from env variables
    local count = tonumber(os.getenv("MY_COUNT"));
    local dstmac = os.getenv("MY_DSTMAC");

    -- set parameters
    pktgen.set(sendport, "burst", burst);
    pktgen.set(sendport, "rate", rate);
    pktgen.set(sendport, "count", count);
    pktgen.set_mac(sendport, "dst", dstmac);

    pktgen.pcap(sendport, "on");
    pktgen.start(sendport);
    pktgen.delay(3000)
    -- spin in a loop till pktgen stops
    while (true) do
        local stats = pktgen.portStats(sendport, "port");
        local sent_count = stats[tonumber(sendport)].opackets;
        if (sent_count == count) then
            break;
        end
        pktgen.delay(1000);
    end
    pktgen.stop(sendport);
    pktgen.quit();
end

main();
